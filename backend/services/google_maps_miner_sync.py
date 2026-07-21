import random
import time
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Page, Browser
from config.mining_config import *


class GoogleMapsMinerSync:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    def initialize(self):
        """Initialize browser"""
        self.playwright = sync_playwright().start()
        browser = self.playwright.chromium.launch(
            headless=BROWSER_HEADLESS,
            args=['--disable-blink-features=AutomationControlled'],
        )
        self.browser = browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = self.browser.new_page()
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def search(self, industry: str, location: str) -> bool:
        """Navigate to Google Maps search"""
        query = f"{industry} {location}".replace(" ", "+")
        url = f"https://www.google.com/maps/search/{query}"
        
        for attempt in range(MAX_RETRIES):
            try:
                self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
                self.page.wait_for_selector('[role="feed"]', timeout=20000)
                time.sleep(3)  # Wait for results to load
                return True
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY_SECONDS)
        return False
    
    def get_business_cards(self):
        """Get all visible business cards in results panel"""
        return self.page.query_selector_all('[role="feed"] > div > div > a')
    
    def scroll_results_panel(self):
        """Scroll the results panel to load more businesses"""
        feed = self.page.query_selector('[role="feed"]')
        if feed:
            feed.evaluate('el => el.scrollBy(0, el.clientHeight)')
            self._human_delay(SCROLL_DELAY_MS)
    
    def click_business_card(self, card):
        """Click a business card and wait for details to load"""
        try:
            card.click()
            self._human_delay(CLICK_DELAY_MS)
            self.page.wait_for_selector('[role="main"]', timeout=ELEMENT_TIMEOUT_MS)
            time.sleep(1)
            return True
        except:
            return False
    
    def extract_business_data(self) -> Optional[Dict[str, Any]]:
        """Extract business information from details panel"""
        try:
            data = {}
            
            name_el = self.page.query_selector('h1')
            data['name'] = name_el.inner_text() if name_el else None
            
            data['google_maps_url'] = self.page.url
            
            rating_el = self.page.query_selector('[role="img"][aria-label*="star"]')
            if rating_el:
                aria_label = rating_el.get_attribute('aria-label')
                if aria_label:
                    try:
                        data['rating'] = float(aria_label.split()[0].replace(',', '.'))
                    except:
                        data['rating'] = None
            
            review_el = self.page.query_selector('button[aria-label*="review"]')
            if review_el:
                aria_label = review_el.get_attribute('aria-label')
                if aria_label:
                    try:
                        data['review_count'] = int(''.join(filter(str.isdigit, aria_label.split()[0])))
                    except:
                        data['review_count'] = None
            
            phone_el = self.page.query_selector('button[data-item-id*="phone"]')
            data['phone'] = phone_el.get_attribute('aria-label') if phone_el else None
            
            website_el = self.page.query_selector('a[data-item-id*="authority"]')
            data['website'] = website_el.get_attribute('href') if website_el else None
            
            address_el = self.page.query_selector('button[data-item-id*="address"]')
            data['address'] = address_el.get_attribute('aria-label') if address_el else None
            
            return data if data.get('name') else None
        except Exception as e:
            return None
    
    def _human_delay(self, delay_range_ms):
        """Random delay to simulate human behavior"""
        delay_ms = random.randint(delay_range_ms[0], delay_range_ms[1])
        time.sleep(delay_ms / 1000)
