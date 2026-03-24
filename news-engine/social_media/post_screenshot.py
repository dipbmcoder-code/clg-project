"""
Social Media Post Screenshot Capture
=====================================
Captures visual screenshots of individual social media posts (X/Twitter & Reddit)
using undetected-chromedriver + BeautifulSoup.

The screenshot is saved to result/img_match/ so it can be picked up by the same
image-handling pipeline used for AI-generated images.

Usage
-----
    from social_media.post_screenshot import capture_post_screenshot

    success = capture_post_screenshot(
        post=post_dict,           # standardised post dict from the pipeline
        output_path="/abs/path/to/img_match/eng_<key>_social_media.png",
        browser=x_browser,        # optional shared XBrowser instance (avoids extra login)
    )
"""

from __future__ import annotations

import os
import sys
import time
import random
import subprocess
import traceback
from pathlib import Path
from typing import Optional, Dict

import requests as http_requests
from PIL import Image
import io

# ── Selenium / UC driver (reuse existing dep) ──
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    _SELENIUM_AVAILABLE = True
except ImportError:
    _SELENIUM_AVAILABLE = False

ROOT = Path(__file__).resolve().parents[1]


def _get_chrome_major_version() -> Optional[int]:
    """Detect installed Chrome major version to avoid driver version mismatch."""
    for cmd in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        try:
            out = subprocess.check_output(
                [cmd, "--version"], stderr=subprocess.DEVNULL, timeout=5
            ).decode()
            for part in reversed(out.strip().split()):
                major = part.split(".")[0]
                if major.isdigit():
                    return int(major)
        except Exception:
            continue
    return None


_CHROME_MAJOR = _get_chrome_major_version()

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_x_post_url(post: Dict) -> Optional[str]:
    """Reconstruct the canonical X.com post URL from post data."""
    permalink = post.get("permalink") or post.get("url")
    if permalink and "x.com" in permalink:
        return permalink

    handler = (post.get("handler") or post.get("source_handle", "")).lstrip("@")
    twitter_id = (post.get("twitter_id") or post.get("post_id", "")).replace("x_", "")
    if handler and twitter_id:
        return f"https://x.com/{handler}/status/{twitter_id}"

    return None


def _build_reddit_post_url(post: Dict) -> Optional[str]:
    permalink = post.get("permalink")
    if permalink and "reddit.com" in permalink:
        return permalink
    return None


def _crop_to_tweet_element(driver, output_path: str) -> bool:
    """
    Scroll to the primary tweet article element, hide distractions,
    then take a clean element screenshot.  Falls back to a full-page
    screenshot cropped to a sensible viewport region.
    """
    try:
        # Wait for the tweet article
        article = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )
        # Scroll it into centre view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", article)
        time.sleep(2)

        # Hide sidebar, suggested follows, trending, promoted tweets
        driver.execute_script("""
            [
              'aside[aria-label]',
              '[data-testid="sidebarColumn"]',
              '[data-testid="trend"]',
              'div[aria-label="Timeline: Trending now"]',
            ].forEach(sel => {
              document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
            });
        """)

        # Take element screenshot (Selenium 4+ supports this natively)
        png_bytes = article.screenshot_as_png
        img = Image.open(io.BytesIO(png_bytes))
        img.save(output_path, "PNG")
        return True

    except Exception as e:
        print(f"  ⚠️ Element screenshot failed: {e}")
        # Fallback: save full-page screenshot
        try:
            driver.save_screenshot(output_path)
            # Crop to upper-middle region (avoids nav bars)
            img = Image.open(output_path)
            w, h = img.size
            cropped = img.crop((0, 80, w, min(h, 800)))
            cropped.save(output_path, "PNG")
            return True
        except Exception as e2:
            print(f"  ❌ Full-page screenshot also failed: {e2}")
            return False


def _screenshot_x_post(post: Dict, output_path: str, browser=None) -> bool:
    """
    Navigate to the X post permalink and capture a clean screenshot.
    Reuses `browser` (XBrowser) if one is already logged in, otherwise
    creates a temporary browser session.
    """
    if not _SELENIUM_AVAILABLE:
        print("⚠️ Selenium not available — skipping X screenshot")
        return False

    url = _build_x_post_url(post)
    if not url:
        print("⚠️ Cannot determine X post URL — skipping screenshot")
        return False

    print(f"  📸 Capturing X post screenshot: {url}")

    def _do_capture(driver) -> bool:
        try:
            driver.get(url)
            time.sleep(random.uniform(4, 6))

            # Accept cookie dialog if shown
            try:
                cookie_btn = driver.find_element(By.XPATH,
                    '//div[@role="button"][.//span[contains(text(), "Accept")]]')
                cookie_btn.click()
                time.sleep(1)
            except Exception:
                pass

            return _crop_to_tweet_element(driver, output_path)

        except WebDriverException as e:
            print(f"  ❌ WebDriver error: {e}")
            return False

    # ── Use shared browser session if available and logged in
    if browser and getattr(browser, "driver", None) and getattr(browser, "logged_in", False):
        return _do_capture(browser.driver)

    # ── Spin up a temporary session
    temp_driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-blink-features=AutomationControlled")

        temp_driver = uc.Chrome(options=options, use_subprocess=True, version_main=_CHROME_MAJOR)
        temp_driver.set_page_load_timeout(60)

        # Try loading saved cookies first
        cookie_file = ROOT / "x_cookies.json"
        if cookie_file.exists():
            try:
                import json
                with open(cookie_file) as f:
                    cookies = json.load(f)
                temp_driver.get("https://x.com")
                time.sleep(2)
                for c in cookies:
                    for k in ["sameSite", "expiry", "storeId"]:
                        c.pop(k, None)
                    try:
                        temp_driver.add_cookie(c)
                    except Exception:
                        pass
            except Exception:
                pass

        return _do_capture(temp_driver)

    except Exception as e:
        print(f"  ❌ Failed to create temp browser: {e}")
        return False
    finally:
        if temp_driver:
            try:
                temp_driver.quit()
            except Exception:
                pass


def _screenshot_reddit_post(post: Dict, output_path: str) -> bool:
    """
    Capture a clean screenshot of a Reddit post using old.reddit.com
    (server-rendered, no JS required — we use requests + PIL to crop).
    Falls back to fetching the post's largest available image.
    """
    url = _build_reddit_post_url(post)
    if not url:
        print("⚠️ Cannot determine Reddit post URL — skipping screenshot")
        return False

    print(f"  📸 Capturing Reddit post screenshot: {url}")

    # Prefer a Selenium screenshot when undetected-chromedriver is available
    if _SELENIUM_AVAILABLE:
        try:
            options = uc.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1280,900")

            driver = uc.Chrome(options=options, use_subprocess=True, version_main=_CHROME_MAJOR)
            driver.set_page_load_timeout(45)
            try:
                # Use old.reddit for simpler, server-rendered layout
                old_url = url.replace("www.reddit.com", "old.reddit.com")
                driver.get(old_url)
                time.sleep(random.uniform(3, 5))

                # Try to screenshot the main entry div
                try:
                    entry = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.thing.link, div.entry")
                        )
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", entry)
                    time.sleep(1)
                    png_bytes = entry.screenshot_as_png
                    img = Image.open(io.BytesIO(png_bytes))
                    img.save(output_path, "PNG")
                    return True
                except TimeoutException:
                    driver.save_screenshot(output_path)
                    img = Image.open(output_path)
                    w, h = img.size
                    img.crop((0, 0, w, min(h, 700))).save(output_path, "PNG")
                    return True

            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

        except Exception as e:
            print(f"  ⚠️ Selenium Reddit screenshot failed: {e}. Trying image download...")

    # ── Fallback: download the first thumbnail image from the post ──
    images = post.get("images") or []
    for img_url in images:
        try:
            resp = http_requests.get(img_url, timeout=15, stream=True)
            resp.raise_for_status()
            img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            img.save(output_path, "PNG")
            print(f"  ✅ Reddit fallback image saved from: {img_url[:70]}")
            return True
        except Exception as e:
            print(f"  ⚠️ Image download attempt failed: {e}")
            continue

    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def capture_post_screenshot(
    post: Dict,
    output_path: str,
    browser=None,
) -> bool:
    """
    Capture a screenshot of a social media post and save it to `output_path`.

    Parameters
    ----------
    post        : Standardised post dict (from reddit_scraper / x_scraper).
    output_path : Absolute path where the PNG should be saved (must end in .png).
    browser     : Optional shared ``XBrowser`` instance that is already logged in.
                  Passing this avoids an extra Chrome launch + X.com login cycle
                  when called from the main pipeline.

    Returns
    -------
    bool : True if a screenshot was successfully saved to `output_path`, else False.
    """
    source = post.get("source", "x").lower()
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if source == "reddit":
            success = _screenshot_reddit_post(post, output_path)
        else:
            success = _screenshot_x_post(post, output_path, browser=browser)

        if success and Path(output_path).is_file() and Path(output_path).stat().st_size > 1000:
            print(f"  ✅ Screenshot saved → {output_path}")
            return True
        else:
            print(f"  ⚠️ Screenshot produced an empty or missing file")
            # Clean up stub
            try:
                if Path(output_path).exists():
                    Path(output_path).unlink()
            except Exception:
                pass
            return False

    except Exception as e:
        print(f"  ❌ Screenshot capture error: {e}")
        traceback.print_exc()
        return False
