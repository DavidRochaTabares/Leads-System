import asyncio
import random
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser
from config.mining_config import *


class GoogleMapsMiner:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def initialize(self):
        """Initialize browser"""
        self.playwright = await async_playwright().start()
        browser = await self.playwright.chromium.launch(
            headless=BROWSER_HEADLESS,
            args=['--disable-blink-features=AutomationControlled'],
        )
        self.browser = await browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = await self.browser.new_page()
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def search(self, industry: str, location: str) -> bool:
        """Navigate to Google Maps search"""
        query = f"{industry} {location}".replace(" ", "+")
        url = f"https://www.google.com/maps/search/{query}"
        
        for attempt in range(MAX_RETRIES):
            try:
                await self.page.goto(url, timeout=PAGE_LOAD_TIMEOUT_MS, wait_until="networkidle")
                await self.page.wait_for_selector('[role="feed"]', timeout=ELEMENT_TIMEOUT_MS)
                await self._human_delay(CLICK_DELAY_MS)
                return True
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(RETRY_DELAY_SECONDS)
        return False
    
    async def get_business_cards(self):
        """Get all visible business cards in results panel"""
        return await self.page.query_selector_all('[role="feed"] > div > div > a')
    
    async def scroll_results_panel(self):
        """Scroll the results panel to load more businesses"""
        feed = await self.page.query_selector('[role="feed"]')
        if feed:
            await feed.evaluate('el => el.scrollBy(0, el.clientHeight)')
            await self._human_delay(SCROLL_DELAY_MS)
    
    async def click_business_card(self, card):
        """Click a business card and wait for details to load"""
        try:
            await card.click()
            await self._human_delay(CLICK_DELAY_MS)
            # Wait for details panel to load
            await self.page.wait_for_selector('[role="main"]', timeout=ELEMENT_TIMEOUT_MS)
            await asyncio.sleep(1)  # Extra wait for dynamic content
            return True
        except:
            return False
    
    async def extract_business_data(self) -> Optional[Dict[str, Any]]:
        """Extract business information from details panel"""
        try:
            data = {}
            
            # Name
            name_el = await self.page.query_selector('h1')
            data['name'] = await name_el.inner_text() if name_el else None
            
            # Google Maps URL
            data['google_maps_url'] = self.page.url
            
            # Rating
            rating_el = await self.page.query_selector('[role="img"][aria-label*="star"]')
            if rating_el:
                aria_label = await rating_el.get_attribute('aria-label')
                if aria_label:
                    try:
                        data['rating'] = float(aria_label.split()[0].replace(',', '.'))
                    except:
                        data['rating'] = None
            
            # Review count
            review_el = await self.page.query_selector('button[aria-label*="review"]')
            if review_el:
                aria_label = await review_el.get_attribute('aria-label')
                if aria_label:
                    try:
                        data['review_count'] = int(''.join(filter(str.isdigit, aria_label.split()[0])))
                    except:
                        data['review_count'] = None
            
            # Phone
            phone_el = await self.page.query_selector('button[data-item-id*="phone"]')
            data['phone'] = await phone_el.get_attribute('aria-label') if phone_el else None
            
            # Website
            website_el = await self.page.query_selector('a[data-item-id*="authority"]')
            data['website'] = await website_el.get_attribute('href') if website_el else None
            
            # Address
            address_el = await self.page.query_selector('button[data-item-id*="address"]')
            data['address'] = await address_el.get_attribute('aria-label') if address_el else None
            
            return data if data.get('name') else None
        except Exception as e:
            return None
    
    async def _human_delay(self, delay_range_ms):
        """Random delay to simulate human behavior"""
        delay_ms = random.randint(delay_range_ms[0], delay_range_ms[1])
        await asyncio.sleep(delay_ms / 1000)
