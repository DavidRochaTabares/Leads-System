import re
from typing import Dict, List, Set
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout


class WebsiteScraper:
    """Simple website scraper for extracting business information"""
    
    PAGES_TO_VISIT = [
        "/",
        "/contact",
        "/contact-us",
        "/about",
        "/about-us",
        "/company",
        "/privacy",
        "/terms"
    ]
    
    def __init__(self, page: Page):
        self.page = page
        self._reset_data()
    
    def _reset_data(self):
        """Reset data for new scrape"""
        self.emails: Set[str] = set()
        self.social_links: Dict[str, str] = {}
        self.features: Dict[str, bool] = {
            "has_chatbot": False,
            "has_whatsapp": False,
            "has_contact_form": False,
            "has_facebook": False,
            "has_instagram": False,
            "has_linkedin": False,
            "has_youtube": False,
            "has_tiktok": False,
            "has_email": False
        }
    
    def scrape(self, website_url: str) -> Dict:
        """Scrape website and return extracted data"""
        # Reset data for new scrape
        self._reset_data()
        
        if not website_url:
            return self._empty_result()
        
        # Normalize URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        try:
            base_url = self._get_base_url(website_url)
            
            # Visit each page
            for path in self.PAGES_TO_VISIT:
                url = base_url + path
                try:
                    self.page.goto(url, timeout=10000, wait_until="domcontentloaded")
                    self.page.wait_for_timeout(1000)
                    self._extract_from_page()
                except PlaywrightTimeout:
                    continue
                except Exception:
                    continue
            
            # Update features based on findings
            self.features["has_email"] = len(self.emails) > 0
            self.features["has_facebook"] = "facebook" in self.social_links
            self.features["has_instagram"] = "instagram" in self.social_links
            self.features["has_linkedin"] = "linkedin" in self.social_links
            self.features["has_youtube"] = "youtube" in self.social_links
            self.features["has_tiktok"] = "tiktok" in self.social_links
            
            return {
                "emails": list(self.emails),
                "social_links": self.social_links,
                "features": self.features,
                "recommended_services": self._generate_recommendations()
            }
        
        except Exception as e:
            return self._empty_result()
    
    def _extract_from_page(self):
        """Extract data from current page"""
        try:
            content = self.page.content()
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, content)
            for email in found_emails:
                # Filter common false positives
                if not any(x in email.lower() for x in ['example.com', 'domain.com', 'email.com']):
                    self.emails.add(email.lower())
            
            # Extract social links
            links = self.page.query_selector_all('a[href]')
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if not href:
                        continue
                    
                    href_lower = href.lower()
                    
                    # Facebook
                    if 'facebook.com' in href_lower and 'facebook' not in self.social_links:
                        self.social_links['facebook'] = href
                    
                    # Instagram
                    elif 'instagram.com' in href_lower and 'instagram' not in self.social_links:
                        self.social_links['instagram'] = href
                    
                    # LinkedIn
                    elif 'linkedin.com' in href_lower and 'linkedin' not in self.social_links:
                        self.social_links['linkedin'] = href
                    
                    # YouTube
                    elif 'youtube.com' in href_lower and 'youtube' not in self.social_links:
                        self.social_links['youtube'] = href
                    
                    # TikTok
                    elif 'tiktok.com' in href_lower and 'tiktok' not in self.social_links:
                        self.social_links['tiktok'] = href
                    
                    # Twitter/X
                    elif ('twitter.com' in href_lower or 'x.com' in href_lower) and 'twitter' not in self.social_links:
                        self.social_links['twitter'] = href
                    
                    # WhatsApp
                    elif any(x in href_lower for x in ['wa.me', 'whatsapp.com', 'whatsapp://']):
                        self.features['has_whatsapp'] = True
                        self.social_links['whatsapp'] = href
                
                except:
                    continue
            
            # Detect contact form
            forms = self.page.query_selector_all('form')
            for form in forms:
                try:
                    form_html = form.inner_html().lower()
                    # Check if form has email or message fields
                    if any(x in form_html for x in ['email', 'message', 'contact', 'name']):
                        self.features['has_contact_form'] = True
                        break
                except:
                    continue
            
            # Detect chatbot
            chatbot_indicators = [
                'intercom', 'drift', 'tawk', 'zendesk', 'livechat', 
                'crisp', 'tidio', 'chatbot', 'messenger', 'whatsapp-widget'
            ]
            content_lower = content.lower()
            for indicator in chatbot_indicators:
                if indicator in content_lower:
                    self.features['has_chatbot'] = True
                    break
        
        except Exception:
            pass
    
    def _generate_recommendations(self) -> List[str]:
        """Generate service recommendations based on features"""
        recommendations = []
        
        if not self.features['has_chatbot']:
            recommendations.append("AI Chatbot")
        
        if not self.features['has_whatsapp']:
            recommendations.append("WhatsApp Automation")
        
        if not self.features['has_contact_form']:
            recommendations.append("Lead Capture System")
        
        if not self.features['has_email']:
            recommendations.append("Website Optimization")
        
        if not self.features['has_facebook'] and not self.features['has_instagram']:
            recommendations.append("Social Media Setup")
        
        return recommendations
    
    def _get_base_url(self, url: str) -> str:
        """Extract base URL from full URL"""
        match = re.match(r'(https?://[^/]+)', url)
        return match.group(1) if match else url
    
    def _empty_result(self) -> Dict:
        """Return empty result structure"""
        return {
            "emails": [],
            "social_links": {},
            "features": self.features,
            "recommended_services": []
        }
