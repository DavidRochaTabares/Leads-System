# -*- coding: utf-8 -*-
import os
import requests
import time
from typing import Dict, Any, Optional
from datetime import datetime


class WhatsAppService:
    """
    WhatsApp Business Cloud API Service
    
    Responsibilities:
    - Send messages via official WhatsApp Business Cloud API
    - Validate API responses
    - Handle errors
    - Update pipeline status
    
    V1: Only sending messages. No replies, follow-ups, or automation.
    """
    
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.business_account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        
        # Rate limiting
        self.min_delay_seconds = int(os.getenv("WHATSAPP_MIN_DELAY_SECONDS", "120"))  # 2 minutes default
        self.last_send_time = 0
        
        # Validate configuration
        if not self.access_token:
            raise ValueError("WHATSAPP_ACCESS_TOKEN not configured")
        if not self.phone_number_id:
            raise ValueError("WHATSAPP_PHONE_NUMBER_ID not configured")
    
    def send_message(self, to_phone: str, message: str) -> Dict[str, Any]:
        """
        Send WhatsApp message via Business Cloud API
        
        Args:
            to_phone: Recipient phone number (with country code, no +)
            message: Message text
        
        Returns:
            {
                'success': bool,
                'message_id': str (if success),
                'error': str (if failed)
            }
        """
        print(f"[WHATSAPP] Sending message to {to_phone}")
        
        # Rate limiting check
        self._enforce_rate_limit()
        
        # Clean phone number - extract only digits
        # Handles formats like: "Teléfono: 305 8260893", "+57 305 826 0893", etc.
        import re
        clean_phone = re.sub(r'[^\d]', '', to_phone)  # Keep only digits
        
        # Validate phone number
        if not clean_phone or len(clean_phone) < 10:
            return {
                'success': False,
                'error': f'Invalid phone number format: {to_phone}'
            }
        
        # Add country code if missing (Colombia by default)
        if len(clean_phone) == 10 and not clean_phone.startswith('57'):
            clean_phone = '57' + clean_phone
            print(f"[WHATSAPP] Added country code: {clean_phone}")
        
        # WhatsApp API endpoint
        url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        # Ensure message is properly encoded
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': clean_phone,
            'type': 'text',
            'text': {
                'body': message
            }
        }
        
        print(f"[WHATSAPP DEBUG] URL: {url}")
        print(f"[WHATSAPP DEBUG] Phone: {clean_phone}")
        print(f"[WHATSAPP DEBUG] Message length: {len(message)} chars")
        print(f"[WHATSAPP DEBUG] Payload: {payload}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"[WHATSAPP DEBUG] Response status: {response.status_code}")
            print(f"[WHATSAPP DEBUG] Response body: {response.text}")
            
            # Update last send time
            self.last_send_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                message_id = data.get('messages', [{}])[0].get('id')
                
                print(f"[WHATSAPP] Message sent successfully. ID: {message_id}")
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'sent_at': datetime.utcnow().isoformat() + 'Z'
                }
            else:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                
                print(f"[WHATSAPP ERROR] {response.status_code}: {error_message}")
                
                return {
                    'success': False,
                    'error': f"WhatsApp API error: {error_message}",
                    'status_code': response.status_code
                }
        
        except requests.exceptions.Timeout:
            print(f"[WHATSAPP ERROR] Request timeout")
            return {
                'success': False,
                'error': 'Request timeout. Please try again.'
            }
        
        except requests.exceptions.RequestException as e:
            print(f"[WHATSAPP ERROR] Request failed: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        
        except Exception as e:
            print(f"[WHATSAPP ERROR] Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between messages"""
        if self.last_send_time > 0:
            elapsed = time.time() - self.last_send_time
            if elapsed < self.min_delay_seconds:
                wait_time = self.min_delay_seconds - elapsed
                print(f"[WHATSAPP] Rate limit: waiting {wait_time:.1f} seconds")
                time.sleep(wait_time)
    
    def send_template_message(self, to_phone: str, template_name: str, variables: list) -> Dict[str, Any]:
        """
        Send WhatsApp template message (for cold outreach)
        
        Args:
            to_phone: Recipient phone number
            template_name: Name of approved template
            variables: List of variable values for template
        
        Returns:
            {
                'success': bool,
                'message_id': str (if success),
                'error': str (if failed)
            }
        """
        print(f"[WHATSAPP] Sending template '{template_name}' to {to_phone}")
        
        # Rate limiting check
        self._enforce_rate_limit()
        
        # Clean phone number
        import re
        clean_phone = re.sub(r'[^\d]', '', to_phone)
        
        # Validate phone number
        if not clean_phone or len(clean_phone) < 10:
            return {
                'success': False,
                'error': f'Invalid phone number format: {to_phone}'
            }
        
        # Add country code if missing (Colombia by default)
        if len(clean_phone) == 10 and not clean_phone.startswith('57'):
            clean_phone = '57' + clean_phone
            print(f"[WHATSAPP] Added country code: {clean_phone}")
        
        # WhatsApp API endpoint
        url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        # Build template payload
        components = []
        if variables:
            components.append({
                'type': 'body',
                'parameters': [
                    {'type': 'text', 'text': str(var)}
                    for var in variables
                ]
            })
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': clean_phone,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {'code': 'es_CO'},
                'components': components
            }
        }
        
        print(f"[WHATSAPP DEBUG] Template URL: {url}")
        print(f"[WHATSAPP DEBUG] Template Phone: {clean_phone}")
        print(f"[WHATSAPP DEBUG] Template Variables: {variables}")
        print(f"[WHATSAPP DEBUG] Template Payload: {payload}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"[WHATSAPP DEBUG] Response status: {response.status_code}")
            print(f"[WHATSAPP DEBUG] Response body: {response.text}")
            
            # Update last send time
            self.last_send_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                message_id = data.get('messages', [{}])[0].get('id')
                
                print(f"[WHATSAPP] Template message sent successfully. ID: {message_id}")
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'sent_at': datetime.utcnow().isoformat() + 'Z'
                }
            else:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                
                print(f"[WHATSAPP ERROR] {response.status_code}: {error_message}")
                
                return {
                    'success': False,
                    'error': f"WhatsApp API error: {error_message}",
                    'status_code': response.status_code
                }
        
        except requests.exceptions.Timeout:
            print(f"[WHATSAPP ERROR] Request timeout")
            return {
                'success': False,
                'error': 'Request timeout. Please try again.'
            }
        
        except requests.exceptions.RequestException as e:
            print(f"[WHATSAPP ERROR] Request failed: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        
        except Exception as e:
            print(f"[WHATSAPP ERROR] Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format"""
        import re
        clean_phone = re.sub(r'[^\d]', '', phone)
        return len(clean_phone) >= 10
