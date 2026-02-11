from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from publication.utils import check_data_exists_in_db
import os, shutil, unicodedata, time, re, json, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class TransfermarktScraper:
    def __init__(self, types):
        self.types = types
        self.base_url = "https://www.flashscore.com" if types == 'where_to_watch' else "https://www.transfermarkt.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            "cache-control": "max-age=0",
        })
        self.driver_pool = []
        self.max_drivers = 3
        self.api_cache = {}
        self.html_cache = {}
        self.cache_ttl = 3600
        self.current_date = datetime.now().strftime('%Y-%m-%d') # current date
        self.yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') # Yesterday date
        self.stop_scrapping = False

        self.endpoints = {
            'transfer': '/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=alle&land_id=&selectedOptionInternalType=nothingSelected&minMarktwert=0&maxMarktwert=500.000.000&minAbloese=0&maxAbloese=500.000.000&yt0=Show',
            'rumour': '/geruechte/aktuellegeruechte/statistik?plus=1',
            'player_abroad': '/detailsuche/spielerdetail/suche',
            'where_to_watch': '/football'
        }

        self.clubs_filename = f'{root_folder}/result/json/scrap_clubs.json'
        self.clubs_data = self.load_from_json(self.clubs_filename) if os.path.exists(self.clubs_filename) else {}

        country_filename = f'{root_folder}/result/json/transfer_market_countries.json'
        # load countries
        self.countries_data = self.load_from_json(country_filename) if os.path.exists(country_filename) else self.scrap_countries(self.base_url+self.endpoints['player_abroad'], country_filename)

    def cached_api_request(self, url, cache_key=None):
        """Cache API responses to avoid duplicate requests"""
        if not cache_key:
            cache_key = url
        
        # Check cache first
        if cache_key in self.api_cache:
            timestamp, data = self.api_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                print(f"Using cached data for: {cache_key}")
                return data
        
        # Make fresh request
        print(f"Making API request to: {url}")
        response = requests.get(url)
        data = response.json()
        
        # Cache the result
        self.api_cache[cache_key] = (time.time(), data)
        return data

    def cached_html_request(self, url, cache_key=None, render_function=None, *args, **kwargs):
        """Cache HTML responses to avoid duplicate rendering"""
        if not cache_key:
            cache_key = url
        
        # Check cache first
        if cache_key in self.html_cache:
            timestamp, html = self.html_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                print(f"Using cached HTML for: {cache_key}")
                return html
        
        # Make fresh request using the provided render function
        print(f"Rendering HTML for: {url}")
        if render_function:
            html = render_function(url, *args, **kwargs)
        else:
            html = self.get_rendered_html(url)
        
        # Cache the result
        if html:
            self.html_cache[cache_key] = (time.time(), html)
        
        return html

    def get_driver(self):
        """Get a driver from pool or create new one"""
        if self.driver_pool:
            return self.driver_pool.pop()
        
        # Regular Chrome driver for other types
        chrome_options = Options()
        chrome_path = shutil.which("chromium-browser") or "/usr/bin/chromium"
        driver_path = shutil.which("chromedriver") or "/usr/local/bin/chromedriver"
        chrome_options.binary_location = chrome_path
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def return_driver(self, driver):
        """Return driver to pool for reuse"""
        if len(self.driver_pool) < self.max_drivers:
            self.driver_pool.append(driver)
        else:
            driver.quit()

    def get_rendered_for_post_html(self, url, country_id):
        """Use Selenium to submit the form via POST - OPTIMIZED with driver reuse"""
        driver = self.get_driver()
        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.get(url)
            driver.delete_all_cookies()
            time.sleep(5)  # Wait for page to load

            # Handle privacy consent iframe if present
            try:
                consent_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title*='consent'], iframe[id*='consent']")
                if consent_iframe:
                    driver.switch_to.frame(consent_iframe)
                    try:
                        accept_button = driver.find_element(By.CSS_SELECTOR, "button[title*='Accept'], button[class*='accept']")
                        accept_button.click()
                        print("Accepted privacy consent")
                    except:
                        pass
                    driver.switch_to.default_content()
                    time.sleep(2)
            except:
                pass  # No consent iframe found

            # Scroll to make form visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            # Select the country in the dropdown using JavaScript
            try:
                driver.execute_script(f"document.getElementById('Detailsuche_zweites_land_id').value = '{country_id}';")
                driver.execute_script("document.getElementById('Detailsuche_zweites_land_id').dispatchEvent(new Event('change'));")
                time.sleep(1)
            except Exception as e:
                print(f"Error selecting country with JS: {e}")
                return None

            # Submit the form using JavaScript
            try:
                driver.execute_script("document.querySelector('form#spieler-detail-suche').submit();")
                time.sleep(3)  # Wait for results to load
            except Exception as e:
                print(f"Error submitting form: {e}")
                return None

            html = driver.page_source
            return html
        finally:
            self.return_driver(driver)

    def get_rendered_html(self, url, wait_time=1, wait_for_element=None):
        """Use Selenium to get page HTML after JS loads - OPTIMIZED with driver reuse"""
        driver = self.get_driver()
        print("url", url)
        try:
            driver.get(url)
            driver.delete_all_cookies()
            
            # Handle privacy consent iframe if present
            try:
                consent_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title*='consent'], iframe[id*='consent']")
                if consent_iframe:
                    driver.switch_to.frame(consent_iframe)
                    try:
                        accept_button = driver.find_element(By.CSS_SELECTOR, "button[title*='Accept'], button[class*='accept']")
                        accept_button.click()
                        print("Accepted privacy consent")
                    except:
                        pass
                    driver.switch_to.default_content()
                    time.sleep(2)
                
            except:
                pass  # No consent iframe found
            
            # If specific element is requested, wait for it to load
            if wait_for_element:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, wait_for_element))
                    )
                    print(f"✓ Element {wait_for_element} loaded successfully")
                except Exception as e:
                    print(f"⚠ Warning: Element {wait_for_element} not found within timeout: {e}")
            driver.execute_script("""
                const el = document.querySelector('section.wcl-summaryTvStreaming_L1-dh > article .wcl-links_7yMDN button')
                if(el) el.click()
            """)
            time.sleep(1)
            html = driver.page_source
            return html
        finally:
            self.return_driver(driver)
  
    def get_total_pages(self, url, types, country_id= 0):
        """Get total number of pages available"""
        try:
            if types == 'player_abroad':
                html = self.get_rendered_for_post_html(url, country_id)
            else:
                html = self.get_rendered_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            pagination = soup.find('ul', {'class': 'tm-pagination'})
            total_pages = 1
            if pagination:
                page_links = pagination.find_all('a', {'class': 'tm-pagination__link'})
                if page_links and len(page_links) > 2:
                    total_pages = int(page_links[-3].text.strip())
            return soup, total_pages
            
        except Exception as e:
            print(f"Error getting total pages: {e}")
            return None, 1
    
    def process_country_player_abroad(self, country, base_url, types, db_data):
        """Process a single country for player abroad scraping"""
        country_results = []
        
        country_id = next(
            (c["id"] for c in self.countries_data if c["name"].lower() == country.lower()),
            None
        )
        if not country_id:
            print(f"Country {country} not found in available countries")
            return country_results
            
        print(f"Scraping players from {country} (ID: {country_id})")
        soup, total_pages = self.get_total_pages(base_url, types, country_id)
        print(f"Found {total_pages} pages to scan for {country}")
        
        for page in range(1, total_pages + 1):
            if self.stop_scrapping:
                break
            print(f"Scanning page {page}/{total_pages} for {country}...")
            page_url = f"{base_url}?page={page}"
            page_results = self.scrape_page(page_url, types, db_data, country_id, soup)
            
            if page_results:
                country_results.extend(page_results)
                print(f"  ✓ Found {len(page_results)} players from {country} on page {page}")
            else:
                print(f"  ✗ Failed to scrape page {page} for {country}")
            
            time.sleep(1.5)
        
        return country_results

    def scrape_all_pages_current_date(self, types, db_data, countries, leagues):
        """Scrape data from all pages but only current date"""
        all_current_date_data = []
        # Check if file already exists
        if types == 'player_abroad':
            all_current_date_data = db_data
        else:
            json_filename = f'{root_folder}/result/json/scrap_{types}s.json'
            if os.path.exists(json_filename):
                print(f"File already exists. Loading data from file...")
                all_current_date_data = self.load_from_json(json_filename)
                if types == 'where_to_watch':
                    league_ids = {d['league']['id'] for d in leagues}
                    all_current_date_data = [d for d in all_current_date_data if d['league']['id'] in league_ids and d['seasons'][0]['year'] == date.today().year]
                else:
                    all_current_date_data = [d for d in all_current_date_data if d['player']['scrap_date'] in (self.current_date, self.yesterday_date)]

        base_url = self.base_url + self.endpoints.get(types, '')
        
        pages_with_current_date = 0
        if types == 'where_to_watch':
            existing_ids = {d['league']['id'] for d in all_current_date_data}
            for league in leagues:
                league_id = league['league']['id']
                if league_id in existing_ids:
                    continue
                # Generate slug safely and efficiently
                league_name = league['league']['name'].lower()
                normalized = unicodedata.normalize("NFKD", league_name)
                ascii_string = normalized.encode("ascii", "ignore").decode("utf-8")
                print('league name', ascii_string)
                league_data = self._search_league(ascii_string, league['country']['name'])
                if not league_data:
                    print(f"Failed to search league {ascii_string}")
                    continue

                new_base_url = f"{base_url}/?r=2:{league_data["id"]}"

                # Scrape and append results efficiently
                page_results = self.scrape_page(new_base_url, types, db_data, countries)
                if not page_results:
                    continue

                scrap_date = self.current_date
                all_current_date_data.extend({**league, 'tv_channels': p, 'scrap_date': scrap_date} for p in page_results)

                existing_ids.add(league_id)

        elif types == 'player_abroad':            
            # Process countries in parallel
            print(f"Processing {len(countries)} countries in batch...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_country = {
                    executor.submit(self.process_country_player_abroad, country, base_url, types, db_data): country 
                    for country in countries
                }
                
                for future in as_completed(future_to_country):
                    country = future_to_country[future]
                    try:
                        country_results = future.result()
                        all_current_date_data.extend(country_results)
                        print(f"✓ Completed scraping for {country}: {len(country_results)} players")
                    except Exception as e:
                        print(f"✗ Failed to process country {country}: {e}")
        else:
            soup, total_pages = self.get_total_pages(base_url, types)
            print(f"Found {total_pages} pages to scan for {types}s on {self.current_date}")
            
            # Collect all current date results first
            all_current_date_results = []
            
            for page in range(1, total_pages + 1):
                print(f"Scanning page {page}/{total_pages} for {self.current_date} {types}s...")
                pages_with_current_date += 1
                page_url = f"{base_url}&page={page}"
                page_results = self.scrape_page(page_url, types, db_data, countries, soup)
                soup = None
                if page_results:
                    # Filter for current date transfers only
                    current_date_results = page_results
                    
                    if current_date_results:
                        all_current_date_results.extend(current_date_results)
                        print(f"  ✓ Found {len(current_date_results)} {types}s on {self.current_date}")
                    else:
                        print(f"  ✗ No {types}s on {self.current_date} found on this page")
                else:
                    print(f"  ✗ Failed to scrape page {page}")
                if self.stop_scrapping: break
                time.sleep(1.5)
            
            # Process all player details in batch instead of sequentially
            if all_current_date_results:
                print(f"\nScraping detailed information for {len(all_current_date_results)} players in batch...")

                filtered_results = []
                seen = set((item["player"]["id"], item[types]["from_club"]["name"], item[types]["to_club"]["name"]) for item in all_current_date_data)
                for item in all_current_date_results:
                    key = (item["player"]["id"], item[types]["from_club"]["name"], item[types]["to_club"]["name"])
                    if key not in seen:
                        filtered_results.append(item)

                detailed_results = self.scrape_player_details_batch(filtered_results)
                all_current_date_data.extend(detailed_results)
            else:
                print("No current date results to process")

            self.save_to_json(self.clubs_data, self.clubs_filename)

        return all_current_date_data, pages_with_current_date

    def scrape_player_details_batch(self, transfer_data_list, batch_size=10, max_workers=3):
        """Scrape multiple player details in parallel with configurable batch size"""
        if not transfer_data_list:
            return []
        
        print(f"Scraping details for {len(transfer_data_list)} players in batches of {batch_size}...")
        
        all_detailed_results = []
        total_successful = 0
        total_failed = 0
        
        # Process in smaller batches to avoid overwhelming the server
        for i in range(0, len(transfer_data_list), batch_size):
            batch = transfer_data_list[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(transfer_data_list)-1)//batch_size + 1}...")
            
            batch_results = []
            successful = 0
            failed = 0
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_player = {
                    executor.submit(self.scrape_player_details, transfer_data): transfer_data 
                    for transfer_data in batch
                }
                
                for future in as_completed(future_to_player):
                    transfer_data = future_to_player[future]
                    player_name = transfer_data['player']['name']
                    
                    try:
                        result = future.result()
                        batch_results.append(result)
                        successful += 1
                        print(f"  ✓ {player_name}")
                    except Exception as e:
                        failed += 1
                        print(f"  ✗ {player_name}: {e}")
                        batch_results.append(transfer_data)  # Keep original data
            
            all_detailed_results.extend(batch_results)
            total_successful += successful
            total_failed += failed
            
            # Small delay between batches to be respectful to the server
            if i + batch_size < len(transfer_data_list):
                time.sleep(2)
        
        print(f"Batch scraping completed: {total_successful} successful, {total_failed} failed out of {len(transfer_data_list)} total")
        return all_detailed_results
    
    def scrape_player_details(self, transfer_data):
        """Scrape detailed player information from player profile URL with caching"""
        player_url = transfer_data['player']['url']

        if not player_url or player_url == 'N/A':
            return transfer_data
        
        try:
            print(f"  Scraping player details: {transfer_data['player']['name']}")
            
            # Use cached HTML for player profile
            cache_key = f"player_{transfer_data['player']['id']}"
            html = self.cached_html_request(player_url, cache_key)
            
            if not html:
                print(f"Failed to get HTML for player: {transfer_data['player']['name']}")
                return transfer_data
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract detailed player information
            player_details = self._extract_player_profile_details(soup, transfer_data['player']['id'])
            
            # Merge with existing transfer data
            transfer_data['player'].update(player_details)
            
            return transfer_data
            
        except Exception as e:
            print(f"Error scraping player details from {player_url}: {e}")
            return transfer_data
    
    def _extract_player_profile_details(self, soup, player_id):
        """Extract detailed information from player profile page"""
        details = {}
        print("finding details")
        try:
            # Player header section
            header = soup.find('header', {'class': 'data-header'})
            if header:
                # Current club
                current_club_elem = header.find('span', {'class': 'data-header__club'})
                if current_club_elem:
                    details['current_club'] = current_club_elem.find('a').text.strip() if current_club_elem.find('a') else current_club_elem.text.strip()
                
                # Shirt number
                shirt_number = header.find('span', {'class': 'data-header__shirt-number'})
                if shirt_number:
                    details['shirt_number'] = shirt_number.text.strip().replace('#', '')
                
                # Market value
                market_value_wrapper = header.find('a',{'class':'data-header__market-value-wrapper'})
                if market_value_wrapper:
                    # updated date
                    last_update_tag = market_value_wrapper.select_one(".data-header__last-update")
                    if last_update_tag:
                        details['last_update_mv'] = self.format_transfermarkt_date(last_update_tag.get_text(strip=True).replace("Last update: ", ""))
                        last_update_tag.extract()
                    # value
                    details['market_value'] = market_value_wrapper.get_text(strip=True, separator="")

            # Player data section - this is where we get most details
            data_table = soup.find('div', {'class': 'info-table'})
            if data_table:
                spans = data_table.select(':scope > span')
                for idx, row in enumerate(spans):
                    if idx % 2 != 0:
                        continue  # Skip odd-indexed spans, process only even ones
                    key = row.text.strip().lower().replace(':', '').replace(' ', '_').replace('/', '_').replace('-', '_')
                    # The value is in the next span (not the current one)
                    if idx + 1 < len(spans):
                        value = spans[idx + 1].text.strip()
                    else:
                        value = row.text.strip()
                    if key == 'date_of_birth_age':
                        dob_info = self._extract_dob_and_birthplace(value)
                        details.update(dob_info)
                    elif key == 'height':
                        details['height'] = value
                    elif key == 'citizenship':
                        nationalities = self._extract_nationalities(spans[idx + 1])
                        details['nationalities'] = nationalities
                    elif key == 'foot':
                        details['preferred_foot'] = value
                    elif key == 'position':
                        details['main_position'] = value
                    elif key == 'current_club':
                        details['national_team'] = value.replace(':', '').strip()
                    elif key == 'joined':
                        details['date_of_joined'] = self.format_transfermarkt_date(value)
                    elif key == 'contract_expires':
                        details['contract_expires'] = self.format_transfermarkt_date(value)
                    elif key == 'place_of_birth':
                        details['place_of_birth'] = value
                    elif key == 'social_media':
                        details['social_media'] = self._extract_social_links(spans[idx + 1])
            
            # Transfer History - now with proper JS wait
            transfer_history = self._extract_transfer_history(player_id)
            if transfer_history:
                details['transfer_history'] = transfer_history

            # Market value history
            market_values = self._extract_market_value_history(player_id)
            if market_values:
                details['market_value_history'] = market_values
            
            # Career stats
            # career_stats = self._extract_career_stats(soup)
            # if career_stats:
            #     details['career_stats'] = career_stats
            
        except Exception as e:
            print(f"Error extracting player profile details: {e}")
        
        return details
    
    def _extract_transfer_history(self, player_id):
        transfer_history = {}
        
        try:
            transfer_api_url = f"https://tmapi-alpha.transfermarkt.technology/transfer/history/player/{player_id}"
            result = self.cached_api_request(transfer_api_url, f"transfer_{player_id}")
            
            if result.get('success', False) and result.get('data', None):
                data = result['data']
                
                # Collect ALL club IDs first
                all_club_ids = set(data.get('clubIds', []))
                
                # Get only missing clubs
                missing_clubs = self.get_missing_clubs(list(all_club_ids))
                
                if missing_clubs:
                    print(f"Found {len(missing_clubs)} missing clubs out of {len(all_club_ids)} total clubs")
                    self._extract_club_data(missing_clubs)
                else:
                    print(f"All {len(all_club_ids)} clubs already cached")
                
                # Now process the transfers with club data available
                transfer_history = self._process_transfer_data(data.get('history', {}))
        except Exception as e:
            print(f"Error extracting transfer history: {e}")
        
        return transfer_history
    
    def _process_transfer_data(self, history_data):
        """Process transfer data with proper error handling"""
        transfer_history = {}
        
        try:
            # Process terminated transfers
            terminated_data = []
            for t in history_data.get('terminated', []):
                try:
                    transfer_record = {
                        "from_club": {
                            "id": t.get('transferSource', {}).get('clubId'),
                            "name": self.clubs_data.get(str(t.get('transferSource', {}).get('clubId')), {}).get('name', 'Without Club'),
                            "country_id": t.get('transferSource', {}).get('countryId'),
                            "country": next(
                                (c["name"] for c in self.countries_data 
                                if int(c["id"]) == int(t.get('transferSource', {}).get('countryId', 0))),
                                None
                            ) if t.get('transferSource', {}).get('countryId') else None
                        },
                        "to_club": {
                            "id": t.get('transferDestination', {}).get('clubId'),
                            "name": self.clubs_data.get(str(t.get('transferDestination', {}).get('clubId')), {}).get('name', 'Without Club'),
                            "country_id": t.get('transferDestination', {}).get('countryId'),
                            "country": next(
                                (c["name"] for c in self.countries_data 
                                if int(c["id"]) == int(t.get('transferDestination', {}).get('countryId', 0))),
                                None
                            ) if t.get('transferDestination', {}).get('countryId') else None
                        },
                        "date": t.get('details', {}).get('date'),
                        "season": t.get('details', {}).get('season'),
                        "fee_transfer": t.get('typeDetails', {})
                    }
                    terminated_data.append(transfer_record)
                except Exception as e:
                    print(f"Error processing terminated transfer: {e}")
                    continue
            
            if terminated_data:
                transfer_history['transfers'] = terminated_data
            
            # Process pending transfers
            pending_data = []
            for t in history_data.get('pending', []):
                try:
                    pending_record = {
                        "from_club": {
                            "id": t.get('transferSource', {}).get('clubId'),
                            "name": self.clubs_data.get(str(t.get('transferSource', {}).get('clubId')), {}).get('name', 'Unknown Club'),
                            "country_id": t.get('transferSource', {}).get('countryId'),
                            "country": next(
                                (c["name"] for c in self.countries_data 
                                if int(c["id"]) == int(t.get('transferSource', {}).get('countryId', 0))),
                                None
                            ) if t.get('transferSource', {}).get('countryId') else None
                        },
                        "to_club": {
                            "id": t.get('transferDestination', {}).get('clubId'),
                            "name": self.clubs_data.get(str(t.get('transferDestination', {}).get('clubId')), {}).get('name', 'Unknown Club'),
                            "country_id": t.get('transferDestination', {}).get('countryId'),
                            "country": next(
                                (c["name"] for c in self.countries_data 
                                if int(c["id"]) == int(t.get('transferDestination', {}).get('countryId', 0))),
                                None
                            ) if t.get('transferDestination', {}).get('countryId') else None
                        },
                        "date": t.get('details', {}).get('date'),
                        "season": t.get('details', {}).get('season'),
                        "fee_transfer": t.get('typeDetails', {})
                    }
                    pending_data.append(pending_record)
                except Exception as e:
                    print(f"Error processing pending transfer: {e}")
                    continue
            
            if pending_data:
                transfer_history['upcoming_transfer'] = pending_data
                
            print(f"Processed {len(terminated_data)} terminated transfers and {len(pending_data)} pending transfers")
            
        except Exception as e:
            print(f"Error in _process_transfer_data: {e}")
            import traceback
            traceback.print_exc()
        
        return transfer_history

    def format_transfermarkt_date(self, date_text):
        """
        Convert date text like '16.02.2005 (20)' or '16.02.2005' to '15 Jan 1999' format.
        Returns None if not matched.
        """
        match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_text)
        if match:
            day, month, year = match.groups()
            try:
                dt = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
                return dt.strftime("%d %b %Y")
            except Exception:
                return None
        return None
    
    def _extract_dob_and_birthplace(self, text):
        result = {}
        try:
            result['date_of_birth_text'] = text

            # Try dd.mm.yyyy format first
            dob_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', text)
            if dob_match:
                day, month, year = dob_match.groups()
                dob_str = f"{day}.{month}.{year}"
                result['date_of_birth'] = self.format_transfermarkt_date(dob_str)
                try:
                    dob_date = datetime.strptime(dob_str, '%d.%m.%Y')
                    age = (datetime.now() - dob_date).days // 365
                    result['calculated_age'] = age
                except Exception as e:
                    pass
            else:
                dob_match = re.search(r'(\d{2})\/(\d{2})\/(\d{4})', text)
                if dob_match:
                    day, month, year = dob_match.groups()
                    dob_str = f"{day}.{month}.{year}"
                    result['date_of_birth'] = self.format_transfermarkt_date(dob_str)
                    try:
                        dob_date = datetime.strptime(dob_str, '%d.%m.%Y')
                        age = (datetime.now() - dob_date).days // 365
                        result['calculated_age'] = age
                    except Exception as e:
                        pass

        except Exception as e:
            print(f"Error extracting DOB and birthplace: {e}")

        return result
    
    def _extract_nationalities(self, td_element):
        """Extract multiple nationalities from the TD element"""
        nationalities = []
        try:
            # Get all nationality flags/images
            flags = td_element.find_all('img')
            for flag in flags:
                nationality = flag.get('title', '').strip()
                if nationality and nationality not in nationalities:
                    nationalities.append(nationality)
            
            # Also check text content for additional nationalities
            text = td_element.get_text(strip=True)
            if text and not flags:  # If no flags but text exists
                nationalities = [text]
            elif flags and text:
                # Sometimes text contains additional info
                flag_countries = [flag.get('title', '') for flag in flags]
                text_parts = [part.strip() for part in text.split(',')]
                for part in text_parts:
                    if part and part not in flag_countries and part not in nationalities:
                        nationalities.append(part)
            
        except Exception as e:
            print(f"Error extracting nationalities: {e}")
        
        return nationalities if nationalities else ['N/A']
    
    def _extract_market_value_history(self, player_id):
        """Extract market value history with batch club processing"""
        market_values = []
        
        try:
            market_value_url = f"https://tmapi-alpha.transfermarkt.technology/player/{player_id}/market-value-history"
            response = requests.get(market_value_url)
            result = response.json()
            
            if result.get('success', False) and result.get('data', None):
                data = result['data']
                
                # Collect all club IDs for batch processing
                club_ids = set(data.get('clubIds', []))

                # Get only missing clubs
                missing_clubs = self.get_missing_clubs(list(club_ids))
                
                if missing_clubs:
                    print(f"Found {len(missing_clubs)} missing clubs out of {len(club_ids)} total clubs")
                    self._extract_club_data(missing_clubs)
                
                # Process market values
                for h in data.get('history', []):
                    market_value_record = {
                        "club_id": h['clubId'],
                        "name": self.clubs_data.get(str(h['clubId']), {}).get('name', 'Without Club'),
                        "age": h['age'],
                        **h['marketValue']
                    }
                    market_values.append(market_value_record)
                    
        except Exception as e:
            print(f"Error extracting market value history: {e}")
        
        return market_values
    
    def _extract_career_stats(self, soup):
        """Extract career statistics"""
        career_stats = []
        try:
            stats_table = soup.find('table', {'class': 'items'})
            if stats_table:
                rows = stats_table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 8:
                        season = cols[0].text.strip()
                        club = cols[3].text.strip()
                        apps = cols[5].text.strip()
                        goals = cols[6].text.strip()
                        
                        career_stats.append({
                            'season': season,
                            'club': club,
                            'appearances': apps,
                            'goals': goals
                        })
        except Exception as e:
            print(f"Error extracting career stats: {e}")
        
        return career_stats
    
    def _extract_social_links(self, element):
        """Extract social media links"""
        social_links = {}
        try:
            if element:
                links = element.find_all('a')
                for link in links:
                    href = link.get('href', '')
                    if 'twitter.com' in href:
                        social_links['twitter'] = href
                    elif 'instagram.com' in href:
                        social_links['instagram'] = href
                    elif 'facebook.com' in href:
                        social_links['facebook'] = href
        except Exception as e:
            print(f"Error extracting social links: {e}")
        
        return social_links

    def scrap_countries(self, url, json_filename):
        try:
            # Clear cookies before making request
            self.session.cookies.clear()
            html = self.get_rendered_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            countries = soup.find('select', {'id': 'Detailsuche_zweites_land_id'})
            if countries:
                country_options = countries.find_all('option')
                data = []
                for country in country_options:
                    country_id = country.get('value',"wrong")
                    country_name = country.text.strip()
                    if country_id:
                        data.append({
                            "id": country_id,
                            'name': country_name
                        })
                self.save_to_json(data, json_filename)
                return data
            else:
                print(f"failed to get countries")
                return []
            
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

    def scrape_page(self, url, types, db_data, country_id=0, soup=None):
        """Scrape data from a single page"""
        try:
            if not soup:
                if types == 'player_abroad':
                    html = self.get_rendered_for_post_html(url, country_id)
                else:
                    html = self.get_rendered_html(url)
                soup = BeautifulSoup(html, 'html.parser')
            
            players_data = []
            rows = soup.select('div.event--leagues.summary-fixtures div.event__match') if types == 'where_to_watch' else soup.select('table.items > tbody > tr')

            for row in rows:
                player_data = self._extract_player_data(row, types, db_data, country_id)
                if player_data:
                    players_data.append(player_data)
                if self.stop_scrapping: break
            return players_data
            
        except Exception as e:
            print(f"Request failed: {e}")
            return []
    
    def _extract_player_data(self, row, types, db_data, country_id=0):
        """Extract individual player data from a table row"""
        columns = [row] if types == 'where_to_watch' else row.find_all('td', recursive=False)
        if len(columns) < 1:
            print("Skipping non-player row:", len(columns))
            return None
        
        try:
            if types == 'where_to_watch':
                name_cell = columns[0].find('a')
                match_url = name_cell.get('href') if name_cell else None

                if not match_url:
                    return None
                
                html = self.get_rendered_html(match_url)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.select('section.wcl-summaryTvStreaming_L1-dh > article .wcl-links_7yMDN .wcl-link_cmXML')

                self.stop_scrapping = True

                if not rows:
                    return None
                
                data = {}

                pattern = re.compile(r"^(.*?)\s*\(([^)]+)\)$")

                for row in rows:
                    a_tag = row.find('a')
                    if not a_tag:
                        continue

                    country_text = a_tag.text.strip()
                    print("country_text", country_text)

                    match = pattern.match(country_text)
                    if not match:
                        continue
                    
                    service, country_codes = match.groups()
                    service = service.strip()
                    codes = [code.strip().lower() for code in country_codes.split("/")]

                    for code in codes:
                        data.setdefault(code, []).append(service)
                    
                return data or None
            elif types == 'player_abroad':
                # For player_abroad, the layout is different
                # Shirt Number, Player, Date of birth/Age, Nat., Club, Height, National player, International matches, Market value
                #     0,          1,         2,             3,     4,    5,      6,                 7,                       8
                
                shirt_number = columns[0].text.strip()
                player_cell = columns[1]
                nested_table = player_cell.select(':scope > table > tr')
                if len(nested_table) < 2:
                    nested_table = player_cell.select(':scope > table > tbody > tr')
                    if len(nested_table) < 2:
                        print("Failed to extract player name and url.")
                        return None
                
                name_cell = nested_table[0].select('td')
                name_cell = name_cell[1].find('a')
                player_name = name_cell.text.strip() if name_cell else 'N/A'
                player_url = self.base_url + name_cell['href'] if name_cell else 'N/A'
                player_id = int(self._extract_player_id(player_url))
                if player_id and check_data_exists_in_db(db_data, player_id, 'player_id'):
                    print(f"Found existing player: {player_id} {player_name}")
                    self.stop_scrapping = True
                    return None
                
                position = nested_table[1].get_text().strip()
                
                # Date of birth / age is in the third column (index 2)
                date_of_birth_text = columns[2].text.strip()
                date_of_birth_result = {}
                if date_of_birth_text:
                    date_of_birth_result = self._extract_dob_and_birthplace(date_of_birth_text)
                
                # Nationality is in the fourth column (index 3)
                nationality_imgs = columns[3].select('img')
                nationality = ",".join([img['title'] for img in nationality_imgs if img and img.has_attr('title')])
                if not nationality:
                    return None
                
                # Club is in the fifth column (index 4)
                club_cell = columns[4].find('a')
                club_url = self.base_url + club_cell.get('href') if club_cell else None
                club_id = self._extract_club_id(club_url) if club_url else 0
                club_cell = club_cell.find('img') if club_cell else None
                club_name = club_cell.get('title') if club_cell else 'Without Club'
                
                # Height is in the sixth column (index 5)
                height = columns[5].text.strip()
                # Market value is in the ninth column (index 8)
                market_value = columns[8].get_text(strip=True) if len(columns) > 8 else 'N/A'
                player_data = {
                    'player_id': player_id,
                    'name': player_name,
                    'url': player_url,
                    'position': position,
                    **date_of_birth_result,
                    #'age': dob_age, # This contains both date of birth and age
                    'nationality': nationality,
                    'height': height,
                    'shirt_number': shirt_number,
                    'club': {
                        'id': club_id,
                        'name': club_name,
                        'url': club_url
                    },
                    'market_value': market_value,
                    'scrap_date': self.current_date,
                    'country_searched': country_id  # Add country info to identify which search found this player
                }
                return player_data
            else:
                # Extract date first to filter early
                if types == 'transfer':
                    transfer_date = self._extract_result_date(columns[5])
                elif types == 'rumour':
                    transfer_date = self._extract_result_date(columns[7])
                # Only process if it's the current date
                if transfer_date not in (self.current_date, self.yesterday_date):
                    print(f"Found Date: {transfer_date}")
                    if transfer_date < self.yesterday_date:
                        self.stop_scrapping = True
                    return None
                
                # Extract nationality (initial - will be updated with detailed scraping)
                nationality_imgs = columns[2].select('img')
                nationality = [
                    unicodedata.normalize("NFKD", img['title'])
                    .encode("ascii", "ignore")
                    .decode("utf-8")
                    .lower()
                    for img in nationality_imgs 
                    if img and img.has_attr('title')
                ]
                if not any(n in country_id for n in nationality):
                    print(f"Skip country: {nationality}")
                    return None
                
                nationality = ','.join(nationality)
                if not nationality:
                    nationality = 'N/A'

                
                nested_table = columns[0].select(':scope > table > tbody > tr')
                if len(nested_table) < 2:
                    print("Failed to extract player name and url.")
                    return None
                # Extract player name and URL
                name_cell = nested_table[0].find('a')
                player_name = name_cell.text.strip() if name_cell else 'N/A'
                player_url = self.base_url + name_cell['href'] if name_cell else 'N/A'
                player_id = int(self._extract_player_id(player_url))
                
                # Extract position
                position = nested_table[1].get_text().strip()
                # Extract age
                age = columns[1].text.strip()
                if age == '-':
                    age = None
                
                nested_table = columns[3].select(':scope > table tr')
                if len(nested_table) < 2:
                    print("Failed to extract left club and leagues.")
                    return None
                # Extract leaving club
                nested_table_tds = nested_table[0].select(':scope > td')
                if len(nested_table_tds) < 2:
                    print("Failed to extract left club.")
                    return None
                left_club_cell = nested_table_tds[1].find('a')
                left_club = left_club_cell.get_text(strip=True) if left_club_cell else 'N/A'
                left_href = left_club_cell.get('href') if left_club_cell else None
                left_club_url = self.base_url + left_href if left_href else 'N/A'
                left_club_id = self._extract_club_id(left_club_url)
                left_flag_img = nested_table[1].find('img') if len(nested_table) > 1 else None
                left_club_flag = left_flag_img.get('alt', 'N/A') if left_flag_img else 'N/A'

                # Extract leaving league
                left_league_cell = nested_table[1].find('a') if len(nested_table) > 1 else None
                left_league = left_league_cell.text.strip() if left_league_cell else 'N/A'
                left_league_href = left_league_cell.get('href') if left_league_cell else None
                left_league_url = self.base_url + left_league_href if left_league_href else 'N/A'
                
                nested_table = columns[4].select(':scope > table tr')
                if len(nested_table) < 2:
                    print("Failed to extract Joined club and leagues.")
                    return None
                
                # Extract joining club
                nested_table_tds = nested_table[0].select(':scope > td')
                if len(nested_table_tds) < 2:
                    print("Failed to extract joined club.")
                    return None
                joined_club_cell = nested_table_tds[1].find('a')
                joined_club = joined_club_cell.get_text(strip=True) if joined_club_cell else 'N/A'
                joined_href = joined_club_cell.get('href') if joined_club_cell else None
                joined_club_url = self.base_url + joined_href if joined_href else 'N/A'
                joined_club_id = self._extract_club_id(joined_club_url)
                joined_flag_img = nested_table[1].find('img') if len(nested_table) > 1 else None
                joined_club_flag = joined_flag_img.get('alt', 'N/A') if joined_flag_img else 'N/A'

                # Extract joining league
                joined_league_cell = nested_table[1].find('a') if len(nested_table) > 1 else None
                joined_league = joined_league_cell.text.strip() if joined_league_cell else 'N/A'
                joined_league_href = joined_league_cell.get('href') if joined_league_cell else None
                joined_league_url = self.base_url + joined_league_href if joined_league_href else 'N/A'
                

                if types == 'rumour':
                    # Extract last reply
                    last_reply_text = columns[7].get_text(strip=True) if len(columns) > 7 else None
                    if last_reply_text == "-":
                        last_reply_text = None

                # check already scraped player
                for item in db_data:
                    if (
                        item['player_id'] == player_id and
                        item[f"current_{types}"]['to_club']['name'] == joined_club and
                        item[f"current_{types}"]['from_club']['name'] == left_club
                    ):
                        # For RUMOUR: match last reply also
                        if types == 'rumour':
                            print("last_reply_text:", last_reply_text)
                            print("db last_reply_text:", item[f"current_{types}"].get('last_reply_text'))
                            if item[f"current_{types}"].get('last_reply_text') == last_reply_text:
                                print("Found existing rumour:", player_name)
                                self.stop_scrapping = True
                            else:
                                print("Rumour exists but reply changed:", player_name)
                            return None

                        # For NON-RUMOUR → direct stop scraping
                        print("Found existing player:", player_name)
                        self.stop_scrapping = True
                        return None

                print("Found new player:", player_name)
                
                # Extract market value
                market_value = columns[6].get_text(strip=True) if len(columns) > 6 else 'N/A'
                if market_value == '-':
                    market_value = None

                if types == 'transfer':
                    # Extract transfer fee
                    transfer_fee = columns[7].get_text(strip=True) if len(columns) > 7 else 'N/A'
                    if transfer_fee == '-':
                        transfer_fee = None
                
                elif types == 'rumour':
                    # Extract contract expires
                    contract_expires = self.format_transfermarkt_date(columns[5].get_text(strip=True)) if len(columns) > 5 else 'N/A'
                    if contract_expires == '-':
                        contract_expires = None
                    
                    # Extract probability
                    probability = columns[8].get_text(strip=True) if len(columns) > 8 else 'N/A'
                    if probability == '-':
                        probability = None

                player_data = {
                    'player': {
                        'id': player_id,
                        'name': player_name,
                        'url': player_url,
                        'position': position,
                        'age': int(age) if age and age.isdigit() else age,
                        'nationality': nationality,
                        'scrap_date': self.current_date
                    },
                    'metadata': {
                        'source': 'transfermarkt',
                        'scraped_timestamp': datetime.now().isoformat()
                    }
                }
                player_data[types] = {
                    'from_club': {
                        'id': left_club_id,
                        'name': left_club,
                        'url': left_club_url,
                        'flag': left_club_flag
                    },
                    'from_league': {
                        'name': left_league,
                        'url': left_league_url
                    },
                    'to_club': {
                        'id': joined_club_id,
                        'name': joined_club,
                        'url': joined_club_url,
                        'flag': joined_club_flag
                    },
                    'to_league': {
                        'name': joined_league,
                        'url': joined_league_url
                    },
                    'market_value': market_value,
                    'date': transfer_date,
                    'scraped_date': self.current_date
                }

                if types == 'transfer':
                    player_data[types]['fee'] = transfer_fee
                elif types == 'rumour':
                    player_data[types]['contract_expires'] = contract_expires
                    player_data[types]['probability'] = probability
                    player_data[types]['last_reply_text'] = last_reply_text
                return player_data
        except Exception as e:
            print(f"Error extracting data from row: {e}")
            return None
    
    def _extract_result_date(self, cell):
        """Extract date from the row"""
        try:
            #for cell in row.find_all('td'):
            text = cell.get_text(strip=True)
            date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})(?:\s*-\s*(\d{2}):(\d{2}))?', text)
            if date_match:
                day, month, year, hour, minute = date_match.groups()
                return f"{year}-{month}-{day}"
                
            date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', text)
            if date_match:
                day, month, year = date_match.groups()
                return f"{year}-{month}-{day}"
            
            date_match = re.search(r'(\d{2})\/(\d{2})\/(\d{4})', text)
            if date_match:
                day, month, year = date_match.groups()
                return f"{year}-{month}-{day}"
            
            title = cell.get('title', '')
            date_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', title)
            if date_match:
                day, month, year = date_match.groups()
                return f"{year}-{month}-{day}"
            
            return "unknown"
            
        except Exception as e:
            print(f"Error extracting date: {e}")
            return "unknown"
    
    def _extract_player_id(self, url):
        if url and '/profil/spieler/' in url:
            return url.split('/profil/spieler/')[-1].split('/')[0]
        return None
    
    def _extract_club_id(self, url):
        if url and '/verein/' in url:
            return url.split('/verein/')[-1].split('/')[0]
        return None
    
    def _fetch_single_club(self, club_id):
        """Fetch single club data and store in clubs_data with caching"""
        try:
            club_url = f"https://tmapi-alpha.transfermarkt.technology/club/{club_id}"
            club_result = self.cached_api_request(club_url, f"club_{club_id}")
            
            if club_result.get('success', False) and club_result.get('data', None):
                club_data = club_result['data']
                self.clubs_data[club_id] = {
                    "id": club_data['id'],
                    "name": club_data['name'],
                    **club_data['baseDetails'],
                    "country": next(
                        (c["name"] for c in self.countries_data 
                        if int(c["id"]) == int(club_data['baseDetails']['countryId'])),
                        None
                    )
                }
                return True
        except Exception as e:
            print(f"Error fetching club {club_id}: {e}")
        return False

    def _extract_club_data_batch(self, club_ids):
        """Fetch multiple clubs in batch - only those not in self.clubs_data"""
        # Double-check we only process missing clubs (in case of race conditions)
        clubs_to_fetch = [club_id for club_id in club_ids if club_id not in self.clubs_data]
        
        if not clubs_to_fetch:
            print("All clubs already cached, skipping batch fetch")
            return
        
        print(f"Batch fetching {len(clubs_to_fetch)} clubs...")
        
        # Process in batches
        batch_size = 10
        successful_fetches = 0
        failed_fetches = 0
        
        for i in range(0, len(clubs_to_fetch), batch_size):
            batch = clubs_to_fetch[i:i + batch_size]
            current_batch = []
            
            # One final check for each club in the batch
            for club_id in batch:
                if club_id not in self.clubs_data:
                    current_batch.append(club_id)
            
            if not current_batch:
                continue
                
            print(f"Processing batch {i//batch_size + 1}/{(len(clubs_to_fetch)-1)//batch_size + 1} with {len(current_batch)} clubs")
            
            # Use ThreadPoolExecutor for parallel requests
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_club = {
                    executor.submit(self._fetch_single_club, club_id): club_id 
                    for club_id in current_batch
                }
                
                for future in as_completed(future_to_club):
                    club_id = future_to_club[future]
                    try:
                        if future.result():
                            successful_fetches += 1
                        else:
                            failed_fetches += 1
                            print(f"Failed to fetch club {club_id}")
                    except Exception as e:
                        failed_fetches += 1
                        print(f"Exception fetching club {club_id}: {e}")
            
            # Small delay between batches
            if i + batch_size < len(clubs_to_fetch):
                time.sleep(0.5)
        
        print(f"Batch fetch completed: {successful_fetches} successful, {failed_fetches} failed")
    
    def _extract_club_data(self, clubs):
        """Fetch only clubs that are not already in self.clubs_data"""
        if not clubs:
            return
        
        # Use batch processing for multiple clubs
        if len(clubs) > 1:
            self._extract_club_data_batch(clubs)
        else:
            # For single club
            self._fetch_single_club(clubs[0])

    def get_missing_clubs(self, club_ids):
        """Return list of club IDs that are not in self.clubs_data"""
        if not club_ids:
            return []
        
        missing = []
        for club_id in club_ids:
            if club_id and str(club_id) not in self.clubs_data:
                missing.append(str(club_id))
        
        return missing
    
    def _search_league(self, league_name: str, country: str):
        """Search leagues in website with caching (optimized)"""
        try:
            league_name_l = league_name.lower()
            country_l = country.lower()

            continents = {
                "asia", "africa", "north america", "south america",
                "antarctica", "europe", "australia"
            }

            # Format URL
            search_url = (
                f"https://s.livesport.services/api/v2/search/"
                f"?q={league_name}&sport-ids=1&limit=50&types=1"
            )

            # Cached request
            search_data = self.cached_api_request(search_url, f"club_{search_url}") or []

            for item in search_data:
                name = item.get("name", "").lower()
                default_country = item.get("defaultCountry", {}).get("name", "").lower()

                # Exact league match + country match
                if name == league_name_l and (default_country in continents or default_country == country_l):
                    return item

            return None

        except Exception as e:
            print(f"Error searching league {league_name}: {e}")
            return None

    def save_to_json(self, data, filename):
        if not data:
            print("No data to save")
            return False
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            
            # with gzip.open(filename, 'wt', encoding='utf-8') as f:
            #     json.dump(data, f, separators=(',', ':'))

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def load_from_json(self, filename):
        """Load data from existing JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
             
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            return []
    
    def cleanup(self):
        """Clean up all drivers in pool and clear expired cache entries"""
        for driver in self.driver_pool:
            driver.quit()
        self.driver_pool.clear()
        
        # Clear expired cache entries
        current_time = time.time()
        
        # Clear expired API cache
        expired_api_keys = [k for k, (timestamp, _) in self.api_cache.items() 
                        if current_time - timestamp > self.cache_ttl]
        for key in expired_api_keys:
            del self.api_cache[key]
        
        # Clear expired HTML cache  
        expired_html_keys = [k for k, (timestamp, _) in self.html_cache.items() 
                            if current_time - timestamp > self.cache_ttl]
        for key in expired_html_keys:
            del self.html_cache[key]
        
        stats = self.get_cache_stats()
        print(f"Cache stats: {stats['total_cached_items']} items ({stats['api_cached_items']} API, {stats['html_cached_items']} HTML), {stats['estimated_cache_size_kb']:.1f} KB")

    def get_cache_stats(self):
        """Get cache statistics for both API and HTML caches"""
        api_cached = len(self.api_cache)
        html_cached = len(self.html_cache)
        
        api_size = sum(len(str(v)) for v in self.api_cache.values())
        html_size = sum(len(html) for _, (_, html) in self.html_cache.items())
        
        total_size_kb = (api_size + html_size) / 1024
        
        return {
            'api_cached_items': api_cached,
            'html_cached_items': html_cached,
            'total_cached_items': api_cached + html_cached,
            'estimated_cache_size_kb': total_size_kb,
            'api_cache_hits': sum(1 for k in self.api_cache if time.time() - self.api_cache[k][0] < self.cache_ttl),
            'html_cache_hits': sum(1 for k in self.html_cache if time.time() - self.html_cache[k][0] < self.cache_ttl)
        }

    def display_summary(self, data, total_scanned_pages, types):
        if not data:
            print(f"No current date {types}s found")
            return
        
        print(f"\n{'='*80}")
        print("ENHANCED TRANSFERMARKT CURRENT DATE DATA SUMMARY")
        print(f"{'='*80}")
        print(f"{types} date: {self.current_date}")
        print(f"Total {types}s with detailed info: {len(data)}")
        print(f"Pages scanned: {total_scanned_pages}")
        
def scrap_current_date_data(types, db_data, countries = [], leagues = []):
    scraper = TransfermarktScraper(types)
    print(f"Looking for {types}s on: {scraper.current_date}")
    print("-" * 80)
    
    try:
        current_date_results, pages_with_data = scraper.scrape_all_pages_current_date(types, db_data, countries, leagues)
        
        if current_date_results:
            scraper.display_summary(current_date_results, pages_with_data, types)
            
            json_filename = f'{root_folder}/result/json/scrap_{types}s.json'
            success = scraper.save_to_json(current_date_results, json_filename)
            
            if success:
                print(f"\n✅ Successfully saved {len(current_date_results)} enhanced {types}s to {json_filename}")
                return current_date_results
            else:
                print("❌ Failed to save data to JSON file")
        else:
            print(f"❌ No {types}s found for {scraper.current_date}")
        return []
    finally:
        scraper.cleanup()  # Ensure drivers are cleaned up

# if __name__ == "__main__":
#     scrap_current_date_transfers()
