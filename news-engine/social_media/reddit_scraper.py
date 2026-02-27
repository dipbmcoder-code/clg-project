"""
Reddit Scraper Module — requests + BeautifulSoup (Selenium fallback)
Scrapes posts from subreddits using web scraping (no API keys required).
Uses old.reddit.com for reliable, server-rendered HTML parsing.
Returns standardized post objects compatible with the social media pipeline.
"""

import os
import re
import time
import random
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

import requests as http_requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# ── Constants ──
MAX_RETRIES = 2
RETRY_DELAY_BASE = 5  # seconds
PAGE_LOAD_TIMEOUT = 20  # seconds
BETWEEN_SUBREDDIT_DELAY = (5, 12)  # random range in seconds


class RedditWebScraper:
    """Scrapes posts from Reddit using HTTP requests + BeautifulSoup. No API keys or browser needed."""

    def __init__(self):
        self._ua = UserAgent()
        self._session = http_requests.Session()

    # ── Fetch page HTML via HTTP requests ──

    def _get_headers(self) -> Dict[str, str]:
        """Build request headers that mimic a real browser."""
        return {
            "User-Agent": self._ua.chrome,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page with HTTP requests, return parsed soup or None.

        old.reddit.com serves fully rendered HTML — no JavaScript needed.
        """
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self._session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=PAGE_LOAD_TIMEOUT,
                    allow_redirects=True,
                )
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")

                # Validate that we got actual post content
                things = soup.select("div.thing[data-fullname]")
                if things:
                    return soup

                # Check for "over 18" interstitial (NSFW wall)
                over18 = soup.select_one("div.interstitial")
                if over18:
                    print(f"⚠️ r/ requires age-gate bypass, skipping")
                    return None

                # Empty page — may be a dead subreddit or Reddit served an error
                print(f"⚠️ No div.thing elements found (attempt {attempt}/{MAX_RETRIES})")

            except http_requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else "?"
                print(f"⚠️ HTTP {status} on attempt {attempt}/{MAX_RETRIES}: {e}")
                # 429 = rate limited, 503 = overloaded — worth retrying
                if status == 403:
                    print("   ⛔ Forbidden — subreddit may be private or banned")
                    return None

            except http_requests.exceptions.RequestException as e:
                print(f"⚠️ Request error on attempt {attempt}/{MAX_RETRIES}: {e}")

            # Retry with back-off
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAY_BASE * attempt + random.uniform(1, 3)
                print(f"   Retrying in {delay:.0f}s...")
                time.sleep(delay)

        return None

    # ── Parse helpers ──

    @staticmethod
    def _parse_score(thing: BeautifulSoup) -> int:
        """Extract score from a post element."""
        # Try the score element
        score_el = thing.select_one("div.score.unvoted")
        if score_el:
            title = score_el.get("title", "")
            if title and title != "•":
                try:
                    return int(title)
                except ValueError:
                    pass
            text = score_el.get_text(strip=True)
            if text and text != "•":
                return RedditWebScraper._parse_compact_number(text)

        # Fallback: data-score attribute on the thing itself
        data_score = thing.get("data-score")
        if data_score:
            try:
                return int(data_score)
            except ValueError:
                pass

        # Fallback: midcol likes
        likes_el = thing.select_one("div.midcol .score.likes")
        if likes_el:
            title = likes_el.get("title", "0")
            try:
                return int(title)
            except ValueError:
                pass

        return 0

    @staticmethod
    def _parse_compact_number(text: str) -> int:
        """Convert compact strings like '1.2k' or '850' to int."""
        text = text.strip().lower().replace(",", "")
        multiplier = 1
        if text.endswith("k"):
            multiplier = 1000
            text = text[:-1]
        elif text.endswith("m"):
            multiplier = 1_000_000
            text = text[:-1]
        try:
            return int(float(text) * multiplier)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _parse_comment_count(thing: BeautifulSoup) -> int:
        """Extract comment count from the comments link."""
        comments_link = thing.select_one("a.bylink.comments")
        if not comments_link:
            return 0
        text = comments_link.get_text(strip=True).lower()
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    @staticmethod
    def _parse_timestamp(thing: BeautifulSoup) -> Optional[str]:
        """Extract ISO timestamp from post."""
        time_el = thing.select_one("time")
        if time_el and time_el.has_attr("datetime"):
            raw = time_el["datetime"]
            try:
                if raw.endswith("Z"):
                    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                else:
                    dt = datetime.fromisoformat(raw)
                return dt.isoformat()
            except (ValueError, TypeError):
                pass

        # Fallback: data-timestamp (epoch ms)
        data_ts = thing.get("data-timestamp")
        if data_ts:
            try:
                dt = datetime.fromtimestamp(int(data_ts) / 1000, tz=timezone.utc)
                return dt.isoformat()
            except (ValueError, TypeError):
                pass

        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _extract_images(thing: BeautifulSoup, post_url: str) -> List[str]:
        """Extract image URLs from the post."""
        images = []

        # Thumbnail
        thumb = thing.select_one("a.thumbnail img")
        if thumb and thumb.has_attr("src"):
            src = thumb["src"]
            if src and not src.endswith("self_default2.png") and "nsfw" not in src:
                if src.startswith("//"):
                    src = "https:" + src
                images.append(src)

        # Direct image link in the post URL
        href_el = thing.select_one("a.title")
        if href_el and href_el.has_attr("href"):
            href = href_el["href"]
            if any(href.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                images.append(href)
            elif "i.redd.it" in href or "i.imgur.com" in href:
                images.append(href)

        # Preview images from data attributes
        data_url = thing.get("data-url", "")
        if data_url and any(data_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
            if data_url not in images:
                images.append(data_url)

        return list(dict.fromkeys(images))  # de-duplicate, preserve order

    # ── Parse a single post ──

    def _parse_post(self, thing: BeautifulSoup, subreddit_name: str) -> Optional[Dict]:
        """Parse a single div.thing post element into our standardized format."""
        try:
            # Skip stickied / promoted posts
            if "stickied" in thing.get("class", []) or "promoted" in thing.get("class", []):
                return None

            # Post ID
            fullname = thing.get("data-fullname", "")  # e.g. "t3_1abc123"
            post_id_raw = fullname.replace("t3_", "") if fullname.startswith("t3_") else fullname
            if not post_id_raw:
                return None

            # Title
            title_el = thing.select_one("a.title")
            title = title_el.get_text(strip=True) if title_el else ""
            if not title:
                return None

            # Self-text (not available on listing page, only title)
            post_text = title

            # External URL (non-self posts)
            embedded_url = None
            if title_el and title_el.has_attr("href"):
                href = title_el["href"]
                if href and not href.startswith("/r/") and not href.startswith("/"):
                    embedded_url = href

            # Author
            author_el = thing.select_one("a.author")
            author = author_el.get_text(strip=True) if author_el else "[deleted]"

            # Metrics
            score = self._parse_score(thing)
            num_comments = self._parse_comment_count(thing)
            timestamp = self._parse_timestamp(thing)

            # Permalink
            permalink_el = thing.select_one("a.bylink.comments")
            permalink = ""
            if permalink_el and permalink_el.has_attr("href"):
                permalink = permalink_el["href"]
                if permalink.startswith("/"):
                    permalink = f"https://reddit.com{permalink}"
            if not permalink:
                permalink = f"https://reddit.com/r/{subreddit_name}/comments/{post_id_raw}"

            # Images
            images = self._extract_images(thing, embedded_url or permalink)

            # Domain tag (flair)
            domain_el = thing.select_one("span.domain a")
            domain = domain_el.get_text(strip=True) if domain_el else ""

            return {
                # ── Standardized fields (pipeline compatible) ──
                "post_id": f"reddit_{post_id_raw}",
                "source": "reddit",
                "source_handle": f"r/{subreddit_name}",
                "post_title": title,
                "tweet_text": post_text,  # pipeline compat key
                "timestamp": timestamp,
                "replies": num_comments,
                "retweets": 0,  # Reddit has no retweets
                "likes": score,
                "score": score,
                "images": images,
                "videos": [],
                "embedded_url": embedded_url,
                "permalink": permalink,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                # ── Legacy compatibility aliases ──
                "twitter_id": f"reddit_{post_id_raw}",
                "handler": f"r/{subreddit_name}",
                # ── Reddit-specific metadata ──
                "reddit_author": author,
                "reddit_domain": domain,
            }

        except Exception as e:
            print(f"⚠️ Error parsing Reddit post: {e}")
            return None

    # ── Public scraping methods ──

    def get_posts(
        self,
        subreddit_name: str,
        mode: str = "hot",
        limit: int = 25,
        hours_ago: int = 12,
    ) -> List[Dict]:
        """
        Scrape posts from a subreddit.

        Args:
            subreddit_name: Name (without r/)
            mode: 'hot', 'new', 'top', or 'rising'
            limit: Maximum posts to return
            hours_ago: Filter posts older than this (for hot/new modes)

        Returns:
            List of standardized post dicts
        """
        mode_path = "" if mode == "hot" else f"/{mode}/"
        if mode == "top":
            mode_path = "/top/?sort=top&t=day"

        url = f"https://old.reddit.com/r/{subreddit_name}{mode_path}"
        print(f"🔍 Scraping r/{subreddit_name} ({mode}) → {url}")

        soup = self._fetch_page(url)
        if not soup:
            print(f"❌ Failed to fetch r/{subreddit_name}")
            return []

        # Parse all post elements
        things = soup.select("div.thing[data-fullname]")
        if not things:
            print(f"⚠️ No posts found on r/{subreddit_name} (page may have changed structure)")
            return []

        posts = []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_ago) if hours_ago else None

        for thing in things:
            parsed = self._parse_post(thing, subreddit_name)
            if not parsed:
                continue

            # Time filter (skip for 'top' mode which has its own time filter)
            if cutoff and mode in ("hot", "new"):
                try:
                    ts = parsed["timestamp"]
                    if "Z" in ts:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    else:
                        dt = datetime.fromisoformat(ts)
                    if dt < cutoff:
                        continue
                except (ValueError, TypeError):
                    pass

            posts.append(parsed)
            if len(posts) >= limit:
                break

        print(f"✅ Scraped {len(posts)} posts from r/{subreddit_name} ({mode})")
        return posts

    def search_subreddit(
        self,
        subreddit_name: str,
        query: str,
        limit: int = 15,
    ) -> List[Dict]:
        """Search within a subreddit for specific topics."""
        url = f"https://old.reddit.com/r/{subreddit_name}/search?q={query}&restrict_sr=on&sort=relevance&t=day"
        print(f"🔍 Searching r/{subreddit_name} for '{query}'")

        soup = self._fetch_page(url)
        if not soup:
            return []

        things = soup.select("div.thing[data-fullname]")
        posts = []
        for thing in things[:limit]:
            parsed = self._parse_post(thing, subreddit_name)
            if parsed:
                posts.append(parsed)

        print(f"✅ Found {len(posts)} posts matching '{query}' in r/{subreddit_name}")
        return posts


# ── Module-level entry point (called by main_social_media.py) ──

def fetch_reddit_data(
    subreddits: List[str],
    mode: str = "hot",
    limit: int = 25,
    hours_ago: int = 12,
) -> List[Dict]:
    """
    Main entry point — fetch posts from multiple subreddits via web scraping.
    No API keys required.

    Args:
        subreddits: List of subreddit names (without r/)
        mode: 'hot', 'new', 'top', or 'rising'
        limit: Max posts per subreddit
        hours_ago: Time window for hot/new modes

    Returns:
        List of standardized post dicts
    """
    if not subreddits:
        print("⚠️ No subreddits provided")
        return []

    scraper = RedditWebScraper()
    all_posts: List[Dict] = []

    for i, subreddit in enumerate(subreddits):
        subreddit = subreddit.strip().replace("r/", "")
        if not subreddit:
            continue

        try:
            posts = scraper.get_posts(
                subreddit,
                mode=mode,
                limit=limit,
                hours_ago=hours_ago,
            )
            all_posts.extend(posts)
        except Exception as e:
            print(f"❌ Error scraping r/{subreddit}: {e}")

        # Polite delay between subreddits (skip after last one)
        if i < len(subreddits) - 1:
            delay = random.uniform(*BETWEEN_SUBREDDIT_DELAY)
            print(f"⏳ Waiting {delay:.0f}s before next subreddit...")
            time.sleep(delay)

    print(f"\n📊 Total Reddit posts fetched: {len(all_posts)}")
    return all_posts


if __name__ == "__main__":
    test_subs = ["technology", "worldnews"]
    print(f"🚀 Scraping posts from {test_subs}")
    results = fetch_reddit_data(test_subs, mode="hot", limit=5)

    for p in results:
        print(f"  [{p['source_handle']}] {p['post_title'][:60]}... (score: {p['score']})")
