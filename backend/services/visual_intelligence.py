import os
import time
from typing import Dict, List, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout
from supabase import Client
import base64


class VisualIntelligence:
    """Capture visual website intelligence including screenshots and metadata"""
    
    SCREENSHOT_PAGES = {
        "homepage": "/",
        "contact": ["/contact", "/contacto", "/contact-us", "/contactanos"],
        "services": ["/services", "/servicios", "/productos", "/products"],
        "about": ["/about", "/nosotros", "/about-us", "/quienes-somos", "/company"]
    }
    
    DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
    MOBILE_VIEWPORT = {"width": 390, "height": 844}
    
    def __init__(self, page: Page, supabase_client: Client):
        self.page = page
        self.supabase = supabase_client
    
    def capture_website_intelligence(self, company_id: str, website_url: str) -> Dict:
        """
        Capture complete visual intelligence for a website
        Returns metadata and screenshot URLs
        """
        if not website_url:
            return self._empty_result()
        
        # Normalize URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        try:
            result = {
                "screenshots": {},
                "metadata": {},
                "visual_features": {}
            }
            
            # Capture homepage screenshots and metadata
            homepage_data = self._capture_homepage(company_id, website_url)
            result["screenshots"].update(homepage_data["screenshots"])
            result["metadata"] = homepage_data["metadata"]
            result["visual_features"] = homepage_data["visual_features"]
            
            # Capture additional pages
            additional_screenshots = self._capture_additional_pages(company_id, website_url)
            result["screenshots"].update(additional_screenshots)
            
            return result
        
        except Exception as e:
            print(f"Visual intelligence error: {str(e)}")
            return self._empty_result()
    
    def _capture_homepage(self, company_id: str, website_url: str) -> Dict:
        """Capture homepage screenshots and extract metadata"""
        result = {
            "screenshots": {},
            "metadata": {},
            "visual_features": {}
        }
        
        try:
            # Navigate to homepage
            start_time = time.time()
            self.page.goto(website_url, timeout=15000, wait_until="networkidle")
            load_time = time.time() - start_time
            
            # Extract metadata
            result["metadata"] = self._extract_metadata(load_time)
            
            # Extract visual features
            result["visual_features"] = self._extract_visual_features()
            
            # Capture desktop screenshot
            self.page.set_viewport_size(self.DESKTOP_VIEWPORT)
            self.page.wait_for_timeout(500)
            desktop_screenshot = self.page.screenshot(full_page=True, type="png")
            desktop_url = self._upload_screenshot(
                company_id, 
                "homepage-desktop.png", 
                desktop_screenshot
            )
            if desktop_url:
                result["screenshots"]["homepage_desktop"] = desktop_url
            
            # Capture mobile screenshot
            self.page.set_viewport_size(self.MOBILE_VIEWPORT)
            self.page.wait_for_timeout(500)
            mobile_screenshot = self.page.screenshot(full_page=True, type="png")
            mobile_url = self._upload_screenshot(
                company_id,
                "homepage-mobile.png",
                mobile_screenshot
            )
            if mobile_url:
                result["screenshots"]["homepage_mobile"] = mobile_url
            
            # Reset to desktop viewport
            self.page.set_viewport_size(self.DESKTOP_VIEWPORT)
        
        except Exception as e:
            print(f"Homepage capture error: {str(e)}")
        
        return result
    
    def _capture_additional_pages(self, company_id: str, base_url: str) -> Dict:
        """Capture screenshots of additional pages"""
        screenshots = {}
        
        # Reset to desktop viewport
        self.page.set_viewport_size(self.DESKTOP_VIEWPORT)
        
        for page_name, paths in self.SCREENSHOT_PAGES.items():
            if page_name == "homepage":
                continue
            
            # Ensure paths is a list
            if isinstance(paths, str):
                paths = [paths]
            
            # Try each path until one works
            for path in paths:
                try:
                    url = base_url.rstrip('/') + path
                    self.page.goto(url, timeout=10000, wait_until="domcontentloaded")
                    self.page.wait_for_timeout(500)
                    
                    # Check if page exists (not 404)
                    title = self.page.title().lower()
                    if '404' in title or 'not found' in title:
                        continue
                    
                    # Capture screenshot
                    screenshot = self.page.screenshot(full_page=True, type="png")
                    screenshot_url = self._upload_screenshot(
                        company_id,
                        f"{page_name}.png",
                        screenshot
                    )
                    
                    if screenshot_url:
                        screenshots[page_name] = screenshot_url
                        break  # Success, move to next page
                
                except PlaywrightTimeout:
                    continue
                except Exception:
                    continue
        
        return screenshots
    
    def _extract_metadata(self, load_time: float) -> Dict:
        """Extract page metadata"""
        metadata = {
            "page_title": "",
            "meta_description": "",
            "h1": "",
            "favicon": "",
            "logo_detected": False,
            "load_time_seconds": round(load_time, 2)
        }
        
        try:
            # Page title
            metadata["page_title"] = self.page.title()
            
            # Meta description
            meta_desc = self.page.query_selector('meta[name="description"]')
            if meta_desc:
                metadata["meta_description"] = meta_desc.get_attribute("content") or ""
            
            # H1
            h1 = self.page.query_selector('h1')
            if h1:
                metadata["h1"] = h1.inner_text()
            
            # Favicon
            favicon = self.page.query_selector('link[rel*="icon"]')
            if favicon:
                metadata["favicon"] = favicon.get_attribute("href") or ""
            
            # Logo detection (common patterns)
            logo_selectors = [
                'img[alt*="logo" i]',
                'img[class*="logo" i]',
                'img[id*="logo" i]',
                '.logo img',
                '#logo img',
                'header img:first-of-type'
            ]
            
            for selector in logo_selectors:
                logo = self.page.query_selector(selector)
                if logo:
                    metadata["logo_detected"] = True
                    break
        
        except Exception as e:
            print(f"Metadata extraction error: {str(e)}")
        
        return metadata
    
    def _extract_visual_features(self) -> Dict:
        """Extract visual features and UI elements"""
        features = {
            "has_cta_buttons": False,
            "has_floating_whatsapp": False,
            "has_contact_form": False,
            "has_booking_system": False,
            "has_chatbot": False,
            "primary_cta_text": "",
            "color_scheme_detected": False
        }
        
        try:
            # CTA buttons
            cta_selectors = [
                'button:has-text("Contact")',
                'button:has-text("Contacto")',
                'a:has-text("Get Started")',
                'a:has-text("Comenzar")',
                'button:has-text("Buy")',
                'button:has-text("Comprar")',
                '.cta',
                '.btn-primary'
            ]
            
            for selector in cta_selectors:
                try:
                    cta = self.page.query_selector(selector)
                    if cta:
                        features["has_cta_buttons"] = True
                        features["primary_cta_text"] = cta.inner_text()[:50]
                        break
                except:
                    continue
            
            # Floating WhatsApp
            whatsapp_selectors = [
                'a[href*="wa.me"]',
                'a[href*="whatsapp"]',
                '.whatsapp-float',
                '.wa-button'
            ]
            
            for selector in whatsapp_selectors:
                wa = self.page.query_selector(selector)
                if wa:
                    features["has_floating_whatsapp"] = True
                    break
            
            # Contact form
            forms = self.page.query_selector_all('form')
            for form in forms:
                try:
                    form_html = form.inner_html().lower()
                    if any(x in form_html for x in ['email', 'message', 'contact']):
                        features["has_contact_form"] = True
                        break
                except:
                    continue
            
            # Booking system indicators
            booking_keywords = ['calendly', 'booking', 'reserva', 'appointment', 'schedule']
            page_content = self.page.content().lower()
            for keyword in booking_keywords:
                if keyword in page_content:
                    features["has_booking_system"] = True
                    break
            
            # Chatbot
            chatbot_indicators = [
                'intercom', 'drift', 'tawk', 'zendesk', 'livechat',
                'crisp', 'tidio', 'chatbot', 'messenger'
            ]
            for indicator in chatbot_indicators:
                if indicator in page_content:
                    features["has_chatbot"] = True
                    break
        
        except Exception as e:
            print(f"Visual features extraction error: {str(e)}")
        
        return features
    
    def _upload_screenshot(self, company_id: str, filename: str, screenshot_bytes: bytes) -> Optional[str]:
        """Upload screenshot to Supabase Storage and return public URL"""
        try:
            # Storage path
            storage_path = f"companies/{company_id}/{filename}"
            
            # Upload to Supabase Storage
            result = self.supabase.storage.from_("website-screenshots").upload(
                storage_path,
                screenshot_bytes,
                {
                    "content-type": "image/png",
                    "upsert": "true"  # Overwrite if exists
                }
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_("website-screenshots").get_public_url(storage_path)
            
            return public_url
        
        except Exception as e:
            print(f"Screenshot upload error: {str(e)}")
            return None
    
    def _empty_result(self) -> Dict:
        """Return empty result structure"""
        return {
            "screenshots": {},
            "metadata": {},
            "visual_features": {}
        }
