"""
X (Twitter) Scraper — undetected-chromedriver with login support.
Logs into X.com once, then scrapes tweets from multiple profiles.
Saves cookies to avoid repeated logins.
"""

import os
import json
import time
import random
import traceback
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional

from bs4 import BeautifulSoup
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from dotenv import load_dotenv
load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
COOKIE_FILE = ROOT / "x_cookies.json"


# ── Helpers ──

def parse_engagement(text: str) -> int:
    text = text.strip().upper().replace(",", "")
    mult = 1
    if text.endswith("K"):
        mult, text = 1000, text[:-1]
    elif text.endswith("M"):
        mult, text = 1_000_000, text[:-1]
    try:
        return int(float(text) * mult)
    except (ValueError, TypeError):
        return 0


def get_timestamp(time_elem) -> str:
    if time_elem and time_elem.has_attr("datetime"):
        return time_elem["datetime"]
    return datetime.now(timezone.utc).isoformat()


def _type_human(element, text):
    """Type text into an element with human-like delays."""
    element.clear()
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(0.03, 0.08))


# ── XBrowser (undetected-chromedriver) ──

class XBrowser:
    """Chrome session using undetected-chromedriver to bypass bot detection."""

    def __init__(self, headless: bool = False):
        self.driver = None
        self.logged_in = False
        self.headless = headless

    def start(self):
        if self.driver:
            return
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)
        self.driver.set_page_load_timeout(60)
        print("🌐 Chrome started (undetected)")

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
            self.logged_in = False

    # ── Cookie persistence ──

    def _save_cookies(self):
        """Save browser cookies to file for reuse."""
        try:
            cookies = self.driver.get_cookies()
            with open(COOKIE_FILE, "w") as f:
                json.dump(cookies, f)
            print(f"  🍪 Saved {len(cookies)} cookies")
        except Exception as e:
            print(f"  ⚠️ Cookie save error: {e}")

    def _load_cookies(self) -> bool:
        """Load cookies from file and check if still valid."""
        if not COOKIE_FILE.exists():
            print("  🍪 No saved cookies found")
            return False

        try:
            with open(COOKIE_FILE, "r") as f:
                cookies = json.load(f)

            if not cookies:
                return False

            # Navigate to X.com first so cookies can be set for the domain
            self.driver.get("https://x.com")
            time.sleep(3)

            for cookie in cookies:
                # Remove problematic fields
                for key in ["sameSite", "expiry", "storeId"]:
                    cookie.pop(key, None)
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    pass

            # Check if cookies are valid by visiting home
            self.driver.get("https://x.com/home")
            time.sleep(5)

            if "/home" in self.driver.current_url and "login" not in self.driver.current_url:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                    )
                    print("  🍪 Cookies valid — already logged in!")
                    self.logged_in = True
                    return True
                except TimeoutException:
                    # Page loaded to /home but no tweets — might still be OK
                    if "login" not in self.driver.current_url:
                        print("  🍪 Cookies seem valid (at /home)")
                        self.logged_in = True
                        return True

            print("  🍪 Cookies expired, need fresh login")
            return False

        except Exception as e:
            print(f"  ⚠️ Cookie load error: {e}")
            return False

    # ── Login ──

    def login(self, username: str = None, password: str = None) -> bool:
        if self.logged_in:
            return True

        username = username or os.getenv("TWITTER_USERNAME", "").strip().strip('"')
        password = password or os.getenv("TWITTER_PASSWORD", "").strip().strip('"')

        if not username or not password:
            print("❌ X credentials missing")
            return False

        if not self.driver:
            self.start()

        print(f"🔑 Logging into X as @{username}")

        try:
            # Step 0: Try loading saved cookies first
            if self._load_cookies():
                return True

            # Step 0b: Check if already logged in (fresh session)
            self.driver.get("https://x.com/home")
            time.sleep(5)
            if "/home" in self.driver.current_url and "login" not in self.driver.current_url:
                try:
                    WebDriverWait(self.driver, 8).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                    )
                    print("✅ Already logged in")
                    self._save_cookies()
                    self.logged_in = True
                    return True
                except TimeoutException:
                    pass

            # Step 1: Go to login page
            print("  → Opening login page")
            self.driver.get("https://x.com/i/flow/login")
            time.sleep(6)

            # Step 2: Enter username
            print("  → Waiting for username field")
            uinput = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            time.sleep(1.5)
            print("  → Entering username")
            uinput.click()
            time.sleep(0.5)
            _type_human(uinput, username)
            time.sleep(1.5)

            # Click Next — multiple strategies
            print("  → Clicking Next")
            next_clicked = False

            # Strategy 1: Find "Next" by role=button and text content
            try:
                btns = self.driver.find_elements(By.XPATH,
                    '//div[@role="button"][.//span[text()="Next"]]')
                if btns:
                    btns[0].click()
                    next_clicked = True
                    print("  → Clicked Next (role=button)")
            except Exception:
                pass

            # Strategy 2: Find by CSS button with specific text
            if not next_clicked:
                try:
                    btns = self.driver.find_elements(By.XPATH,
                        '//button[.//span[text()="Next"]]')
                    if btns:
                        btns[0].click()
                        next_clicked = True
                        print("  → Clicked Next (button)")
                except Exception:
                    pass

            # Strategy 3: Press Enter
            if not next_clicked:
                uinput.send_keys(Keys.RETURN)
                print("  → Pressed Enter")

            time.sleep(5)
            print(f"  → URL: {self.driver.current_url}")

            # Step 2b: Handle verification challenge
            pwd_found = self._check_password_field()
            if not pwd_found:
                # May need to handle a challenge
                self._handle_challenge(username)
                pwd_found = self._check_password_field()

            if not pwd_found:
                print("❌ Cannot find password field")
                self._debug("no_password")
                return False

            # Step 3: Enter password
            print("  → Entering password")
            pinput = self.driver.find_element(By.CSS_SELECTOR,
                'input[name="password"], input[type="password"]')
            _type_human(pinput, password)
            time.sleep(1)

            # Click Log in
            try:
                login_btn = self.driver.find_element(By.CSS_SELECTOR,
                    '[data-testid="LoginForm_Login_Button"]')
                ActionChains(self.driver).move_to_element(login_btn).pause(0.2).click().perform()
                print("  → Clicked Log in")
            except NoSuchElementException:
                pinput.send_keys(Keys.RETURN)
                print("  → Pressed Enter for login")

            time.sleep(6)

            # Step 4: Verify login
            cur = self.driver.current_url
            print(f"  → Post-login URL: {cur}")

            if "login" not in cur.lower():
                print("✅ Login successful!")
                self._save_cookies()
                self.logged_in = True
                return True

            # Check for tweets
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                )
                print("✅ Login successful (tweets visible)")
                self._save_cookies()
                self.logged_in = True
                return True
            except TimeoutException:
                pass

            if "x.com" in cur:
                print("✅ Login likely OK")
                self._save_cookies()
                self.logged_in = True
                return True

            self._debug("login_uncertain")
            return False

        except Exception as e:
            print(f"❌ Login error: {type(e).__name__}: {e}")
            traceback.print_exc()
            self._debug("login_error")
            return False

    def _check_password_field(self) -> bool:
        """Check if password field is visible."""
        try:
            self.driver.find_element(By.CSS_SELECTOR,
                'input[name="password"], input[type="password"]')
            return True
        except NoSuchElementException:
            return False

    def _handle_challenge(self, username):
        """Handle X verification challenge."""
        # Get email from env for challenge
        email = os.getenv("TWITTER_EMAIL", "").strip().strip('"') or \
                os.getenv("CMS_ADMIN_USER_EMAIL", "").strip().strip('"')

        # Look for challenge input
        challenge = None
        for sel in ['input[data-testid="ocfEnterTextTextInput"]', 'input[name="text"]']:
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, sel)
                # Make sure it's not the initial username field
                try:
                    self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
                    # Still on username page — try clicking Next again with JS
                    print("  → Still on username page, retrying Next via JS")
                    self.driver.execute_script("""
                        var btns = document.querySelectorAll('[role="button"]');
                        for (var b of btns) {
                            if (b.textContent.trim() === 'Next') {
                                b.focus();
                                b.click();
                                return;
                            }
                        }
                    """)
                    time.sleep(5)
                    # Check again
                    if self._check_password_field():
                        return True
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
                        print("  → Next still didn't work")
                        return False
                    except NoSuchElementException:
                        # Username field gone, re-find challenge
                        try:
                            challenge = self.driver.find_element(By.CSS_SELECTOR, sel)
                        except NoSuchElementException:
                            return self._check_password_field()
                except NoSuchElementException:
                    challenge = el
                    break
            except NoSuchElementException:
                continue

        if not challenge:
            return False

        # Try values: email then username
        values = [email, username] if email else [username]
        for val in values:
            print(f"  ⚠️ Challenge — trying: {val[:4]}***")
            try:
                challenge.clear()
                challenge.send_keys(val)
                time.sleep(0.5)
                challenge.send_keys(Keys.RETURN)
                time.sleep(5)
                if self._check_password_field():
                    print("  → Challenge passed!")
                    return True
                try:
                    challenge = self.driver.find_element(By.CSS_SELECTOR,
                        'input[data-testid="ocfEnterTextTextInput"], input[name="text"]')
                except NoSuchElementException:
                    break
            except Exception as ex:
                print(f"  → Challenge error: {ex}")
                break

        return False

    def _debug(self, prefix):
        try:
            path = str(ROOT / f"{prefix}.png")
            self.driver.save_screenshot(path)
            print(f"  📸 {prefix}.png saved")
            # Dump page info
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                try:
                    print(f"  input: type={inp.get_attribute('type')} name={inp.get_attribute('name')} "
                          f"auto={inp.get_attribute('autocomplete')}")
                except Exception:
                    pass
            # Page text hints
            try:
                spans = self.driver.find_elements(By.CSS_SELECTOR, "span, h1, h2")
                hints = []
                for s in spans:
                    t = s.text.strip()
                    if t and 5 < len(t) < 150 and t not in hints:
                        hints.append(t)
                    if len(hints) >= 6:
                        break
                print(f"  hints: {hints}")
            except Exception:
                pass
        except Exception:
            pass

    # ── Scrape profile ──

    def scrape_profile(self, handle: str, max_tweets: int = 15) -> List[Dict]:
        if not self.driver:
            return []

        url = f"https://x.com/{handle}"
        print(f"🔍 Scraping @{handle}")

        try:
            self.driver.get(url)
            time.sleep(5)

            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                )
            except TimeoutException:
                print(f"  ⚠️ No tweets for @{handle}")
                return []

            # Scroll to load more
            for _ in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7)")
                time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            return self._parse_tweets(soup, handle, max_tweets)

        except Exception as e:
            print(f"  ❌ Error scraping @{handle}: {e}")
            return []

    def _parse_tweets(self, soup, handle, max_tweets):
        articles = soup.select('article[data-testid="tweet"]')
        if not articles:
            return []

        tweets = []
        for el in articles[:max_tweets]:
            try:
                text_el = el.select_one('div[data-testid="tweetText"]')
                text = text_el.get_text(" ", strip=True) if text_el else ""
                if not text:
                    continue

                time_el = el.select_one("time")
                tid = self._tweet_id(el)

                tweets.append({
                    "twitter_id": tid,
                    "handler": handle,
                    "tweet_text": text,
                    "tweeted_time": get_timestamp(time_el),
                    "replies": self._metric(el, "reply"),
                    "retweets": self._metric(el, "retweet"),
                    "likes": self._metric(el, "like"),
                    "images": self._images(el),
                    "url": f"https://x.com/{handle}/status/{tid}" if tid else None,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                })
            except Exception:
                continue

        print(f"  ✅ {len(tweets)} tweets from @{handle}")
        return tweets

    @staticmethod
    def _metric(el, name):
        for c in el.select(f'[data-testid*="{name}"]'):
            t = c.get_text(" ", strip=True)
            if t:
                return parse_engagement(t)
        return 0

    @staticmethod
    def _images(el):
        imgs = []
        for img in el.select('img[src*="twimg.com/media"], img[src*="pbs.twimg.com/media"]'):
            imgs.append(img["src"])
        return list(dict.fromkeys(imgs))

    @staticmethod
    def _tweet_id(el):
        link = el.select_one('a[href*="/status/"]')
        if link and link.has_attr("href"):
            for p in reversed(link["href"].split("/")):
                if p.isdigit():
                    return p
        return None


# ── Public API (backward-compatible) ──

class SocialMediaScraper:
    def __init__(self, username, target_date=None, use_json_save=True, browser=None):
        self.username = username
        self.target_date = target_date
        self._browser = browser

    def scrape_tweets(self, max_tweets=15):
        if self._browser and self._browser.driver:
            tweets = self._browser.scrape_profile(self.username, max_tweets=max_tweets)
        else:
            b = XBrowser(headless=False)
            try:
                b.start()
                b.login()
                tweets = b.scrape_profile(self.username, max_tweets=max_tweets)
            finally:
                b.quit()

        if self.target_date and tweets:
            tweets = self._filter(tweets, self.target_date)
        return tweets[:15]

    @staticmethod
    def _filter(tweets, target_date):
        """Filter tweets to keep those from the target date or the day before."""
        if isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return tweets
        from datetime import timedelta
        yesterday = target_date - timedelta(days=1)
        out = []
        for t in tweets:
            try:
                raw = str(t.get("tweeted_time", ""))
                dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                if dt.date() >= yesterday:
                    out.append(t)
            except (ValueError, TypeError):
                out.append(t)
        return out if out else tweets  # If no tweets match dates, return all


def scrap_social_media_data(handlers: List[str]) -> List[Dict]:
    """Scrape tweets from multiple X handles. One browser, one login."""
    if not handlers:
        return []

    all_tweets = []
    browser = XBrowser(headless=False)

    try:
        browser.start()
        if not browser.login():
            print("❌ X login failed")
            return []

        for i, h in enumerate(handlers):
            h = h.strip().replace("@", "")
            if not h:
                continue
            try:
                scraper = SocialMediaScraper(
                    username=h,
                    target_date=datetime.now().strftime("%Y-%m-%d"),
                    browser=browser,
                )
                tweets = scraper.scrape_tweets()
                all_tweets.extend(tweets)
                print(f"  📊 @{h}: {len(tweets)} tweets")
            except Exception as e:
                print(f"  ❌ @{h}: {e}")

            if i < len(handlers) - 1:
                time.sleep(random.uniform(3, 6))
    finally:
        browser.quit()

    print(f"📊 Total: {len(all_tweets)} tweets")
    return all_tweets


if __name__ == "__main__":
    print("🚀 Testing X scraper with undetected-chromedriver")
    results = scrap_social_media_data(["BBCWorld"])
    print(f"\n{len(results)} tweets scraped")
    for t in results[:5]:
        print(f"  @{t['handler']}: {t['tweet_text'][:70]}… (♥{t['likes']})")
