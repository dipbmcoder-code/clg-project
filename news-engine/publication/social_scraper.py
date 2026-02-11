# fixed_social_media_scraper.py
import os, re, json, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from publication.utils import get_timestamp

ROOT = Path(__file__).resolve().parents[1]


def parse_engagement(text):
    """Convert engagement string like '1.2K' to int"""
    text = text.strip().upper().replace(",", "")
    mult = 1
    if text.endswith("K"):
        mult = 1000
        text = text[:-1]
    elif text.endswith("M"):
        mult = 1000000
        text = text[:-1]
    try:
        return int(float(text) * mult)
    except:
        return 0


class SocialMediaScraper:
    def __init__(self, username, target_date=None, use_json_save=True):
        self.username = username
        self.twitter_url = f"https://x.com/{username}"
        self.mobile_url = f"https://mobile.twitter.com/{username}"
        self.target_date = target_date
        self.use_json_save = use_json_save

    def try_requests(self, url):
        try:
            ua = UserAgent().chrome
            resp = requests.get(url, headers={"User-Agent": ua}, timeout=10)
            return resp.text, resp.url, resp.status_code
        except Exception as e:
            return None, url, None

    def get_rendered_html(self, url, wait_seconds=10, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={UserAgent().chrome}")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            WebDriverWait(driver, wait_seconds).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
            )
        except:
            pass

        html = driver.page_source
        cur_url = driver.current_url
        driver.quit()
        return html, cur_url

    def scrape_tweets(self, max_tweets=15):
        print(f"Starting scrape for @{self.username} (target_date={self.target_date})")

        # 1) Try desktop requests
        text, final_url, status = self.try_requests(self.twitter_url)
        soup = None
        if text and status == 200 and "login" not in final_url.lower() and "Sign in" not in text[:800]:
            soup = BeautifulSoup(text, "html.parser")

        # 2) If requests gave no tweets -> Selenium fallback
        if not soup or not soup.select('article[data-testid="tweet"]'):
            print("Requests returned no usable tweets → Using Selenium...")
            html, cur = self.get_rendered_html(self.twitter_url, wait_seconds=12, headless=True)
            soup = BeautifulSoup(html, "html.parser")
            print(f"Selenium loaded (current_url={cur})")

        all_tweets = self.parse_tweets(soup, max_tweets=max_tweets)
        # fresh = self.filter_out_pinned_tweets(all_tweets)
        fresh = all_tweets
        # print(fresh)
        if self.target_date:
            fresh = self.filter_tweets_by_date(fresh, self.target_date)

        if len(fresh) > 10:
            fresh = fresh[:10]

        print(f"Scrape complete — found {len(fresh)} tweets (after filters).")

        # if self.use_json_save:
        #     self.save_to_json(fresh)

        return fresh
   

    def parse_tweets(self, soup, max_tweets=10):
        tweets = []
        tweet_elements = soup.select('article[data-testid="tweet"]')
        if not tweet_elements:
            print("No tweet elements found with selectors.")
            return []

        for el in tweet_elements[:max_tweets]:
            try:
                text_elem = el.select_one('div[data-testid="tweetText"]')
                text = text_elem.get_text(" ", strip=True) if text_elem else "No text content"

                # time_elem = el.select_one("time")
                # # print("time")
                # print(time_elem)
                # timestamp = time_elem["datetime"] if time_elem and time_elem.has_attr("datetime") else datetime.now().isoformat()
                time_elem = el.select_one("time")
                timestamp = get_timestamp(time_elem)

                reply = self.get_metric(el, "reply")
                retweet = self.get_metric(el, "retweet")
                like = self.get_metric(el, "like")

                imgs = self.extract_images(el)
                tweet_id = self.extract_tweet_id(el)
                tweet_url = f"https://twitter.com/{self.username}/status/{tweet_id}" if tweet_id else None

                tweets.append({
                    "twitter_id": tweet_id,
                    "handler": self.username,
                    "tweet_text": text,
                    "tweeted_time": timestamp,
                    "replies": reply,
                    "retweets": retweet,
                    "likes": like,
                    "images": imgs,
                    "url": tweet_url,
                    "scraped_at": datetime.now().isoformat()
                })
            except Exception as e:
                continue
        return tweets

    def extract_images(self, tweet_element):
        images = []
        for img in tweet_element.select('img[src*="twimg.com/media"], img[src*="pbs.twimg.com/media"]'):
            images.append(img["src"])
        return list(dict.fromkeys(images))

    def extract_tweet_id(self, tweet_element):
        link = tweet_element.select_one('a[href*="/status/"]')
        if link and link.has_attr("href"):
            parts = link["href"].split("/")
            for p in reversed(parts):
                if p.isdigit():
                    return p
        return None

    def get_metric(self, el, metric):
        cand = el.select(f'[data-testid*="{metric}"]')
        for c in cand:
            txt = c.get_text(" ", strip=True)
            if txt:
                return parse_engagement(txt)
        return 0

    def filter_out_pinned_tweets(self, tweets):
        non_pinned = []
        for tweet in tweets:
            try:
                t = tweet.get("tweeted_time", "")
                tt = datetime.fromisoformat(t.replace("Z", "+00:00")) if "Z" in t else datetime.fromisoformat(t)
                is_old = (datetime.now() - tt).days > 7
                if is_old and (tweet["likes"] > 1000 or tweet["retweets"] > 100):
                    continue
                non_pinned.append(tweet)
            except:
                non_pinned.append(tweet)
        return non_pinned

    def filter_tweets_by_date(self, tweets, target_date):
        if isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except:
                return tweets
        filtered = []
        for tweet in tweets:
            try:
                t = tweet.get("tweeted_time", "")
                tt = datetime.fromisoformat(t.replace("Z", "+00:00")) if "Z" in t else datetime.fromisoformat(t)
                if tt.date() == target_date:
                    filtered.append(tweet)
            except:
                filtered.append(tweet)
        return filtered

    def save_to_json(self, data, filename=None):
        if not data:
            print("Nothing to save.")
            return False
        if filename is None:
            # filename = ROOT / f"tweets_{self.username}_{self.target_date}.json"
            filename = ROOT / f"result/json/tweets_{self.username}_{self.target_date}.json"
        os.makedirs(filename.parent, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"tweets": data}, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} tweets → {filename}")
        return True

def scrap_social_media_data(handlers):
    """Scrape social media data for multiple handlers"""
    all_tweets = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    # current_date = "2025-09-15"
    
    for handler in handlers:
        try:
            scraper = SocialMediaScraper(username=handler, target_date=current_date)
            tweets = scraper.scrape_tweets()
            
            for tweet in tweets:
                tweet['handler'] = handler
                all_tweets.append(tweet)
                
            time.sleep(10)  # Be respectful with requests
            
        except Exception as e:
            print(f"Error scraping {handler}: {e}")
            continue
    
    return all_tweets
# if __name__ == "__main__":
#     s = SocialMediaScraper("FabrizioRomano", target_date=None)
#     results = s.scrape_tweets()
#     for r in results:
#         print(r)
