#!/usr/bin/env python3
"""
Mobile Security Testing Module
Integrates SMS/Email delivery for mobile penetration testing
Authorized for in-house team testing only
"""

import os
import re
import logging
import json
from datetime import datetime
from typing import Optional, Dict, List
from dotenv import load_dotenv
from database.models import SessionLocal, AttackSimulation, AuditLog

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mobile_testing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MobileSecurityTesting:
    """
    Mobile Security Testing Framework for In-House Team Testing
    Supports iOS and Android security assessments
    """

    def __init__(self):
        self.session = SessionLocal()

        # Load API credentials from environment
        self.textbelt_key = os.getenv('TEXTBELT_API_KEY', 'textbelt')  # 'textbelt' for free tier
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY', '')

        # Infobip API configuration
        self.infobip_api_key = os.getenv('INFOBIP_API_KEY', '')
        self.infobip_base_url = os.getenv('INFOBIP_BASE_URL', 'https://g9vm5e.api.infobip.com')
        self.infobip_from_number = os.getenv('INFOBIP_FROM_NUMBER', '')
        self.infobip_whatsapp_enabled = os.getenv('INFOBIP_WHATSAPP_ENABLED', 'false').lower() == 'true'

        # Testing mode
        self.demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

        # SMS provider selection: 'textbelt' or 'infobip'
        self.sms_provider = os.getenv('SMS_PROVIDER', 'infobip' if self.infobip_api_key else 'textbelt')

        # Regex patterns for input validation
        self.ip_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}:?\d+$")
        self.phone_pattern = re.compile(r"^\+?\d{1,3}\s?\(?\d{1,3}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}$")
        self.email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        # Load authorized targets
        self.authorized_targets = self._load_authorized_targets()

        logger.info("Mobile Security Testing Module initialized")
        logger.info(f"Demo Mode: {self.demo_mode}")
        logger.info(f"SMS Provider: {self.sms_provider}")
        logger.info(f"Infobip WhatsApp: {'Enabled' if self.infobip_whatsapp_enabled else 'Disabled'}")
        logger.info(f"Authorized targets loaded: {len(self.authorized_targets)}")

    def _load_authorized_targets(self) -> List[Dict]:
        """Load authorized targets for testing"""
        try:
            import yaml
            with open('config/mobile_targets.yaml', 'r') as f:
                config = yaml.safe_load(f)
                return config.get('authorized_targets', [])
        except FileNotFoundError:
            logger.warning("mobile_targets.yaml not found, using empty target list")
            return []
        except Exception as e:
            logger.error(f"Error loading authorized targets: {e}")
            return []

    def validate_target_authorization(self, target: str, target_type: str) -> bool:
        """
        Validate that target is authorized for testing

        Args:
            target: Phone number, email, or IP address
            target_type: 'phone', 'email', or 'ip'

        Returns:
            bool: True if authorized, False otherwise
        """
        for authorized in self.authorized_targets:
            if authorized.get('type') == target_type and authorized.get('value') == target:
                if authorized.get('status') == 'active':
                    logger.info(f"Target authorized: {target} ({target_type})")
                    return True

        logger.warning(f"UNAUTHORIZED TARGET BLOCKED: {target} ({target_type})")
        return False

    def detect_target_type(self, target: str) -> Optional[str]:
        """Detect target type from input string"""
        if self.ip_pattern.match(target):
            return 'ip'
        elif self.phone_pattern.match(target):
            return 'phone'
        elif self.email_pattern.match(target):
            return 'email'
        else:
            return None

    def log_test_activity(self, test_type: str, target: str, status: str, details: Dict):
        """Log all testing activities to database and audit trail"""
        try:
            # Log to attack simulations
            attack = AttackSimulation(
                attack_type=f"mobile_testing_{test_type}",
                target=target,
                status=status,
                timestamp=datetime.utcnow(),
                details=json.dumps(details)
            )
            self.session.add(attack)

            # Log to audit trail
            audit = AuditLog(
                action=f"MOBILE_TEST_{test_type.upper()}",
                user="red_team_operator",
                target=target,
                timestamp=datetime.utcnow(),
                details=json.dumps(details),
                ip_address=details.get('operator_ip', 'unknown')
            )
            self.session.add(audit)

            self.session.commit()
            logger.info(f"Test activity logged: {test_type} -> {target} -> {status}")

        except Exception as e:
            logger.error(f"Error logging test activity: {e}")
            self.session.rollback()

    def _send_sms_via_infobip(self, phone_number: str, message: str) -> Dict:
        """
        Send SMS via Infobip API

        Args:
            phone_number: Target phone number
            message: Message content

        Returns:
            Dict with API response details
        """
        try:
            import http.client

            # Parse base URL to get host
            from urllib.parse import urlparse
            parsed_url = urlparse(self.infobip_base_url)
            host = parsed_url.netloc

            # Create connection
            conn = http.client.HTTPSConnection(host)

            # Prepare payload
            payload = json.dumps({
                "messages": [
                    {
                        "from": self.infobip_from_number,
                        "to": phone_number.replace('+', '').replace('-', '').replace(' ', ''),
                        "text": message
                    }
                ]
            })

            # Prepare headers
            headers = {
                'Authorization': f'App {self.infobip_api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            # Send request
            conn.request("POST", "/sms/2/text/advanced", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_data = json.loads(data.decode("utf-8"))

            conn.close()

            # Check response
            if res.status == 200:
                messages = response_data.get('messages', [])
                if messages and messages[0].get('status', {}).get('groupName') == 'PENDING':
                    return {
                        'success': True,
                        'provider': 'infobip',
                        'message_id': messages[0].get('messageId'),
                        'status': messages[0].get('status', {}).get('name'),
                        'response': response_data
                    }

            return {
                'success': False,
                'provider': 'infobip',
                'error': f"API returned status {res.status}",
                'response': response_data
            }

        except Exception as e:
            logger.error(f"Infobip SMS error: {e}")
            return {
                'success': False,
                'provider': 'infobip',
                'error': str(e)
            }

    def _send_whatsapp_via_infobip(self, phone_number: str, message: str, template_name: str = None) -> Dict:
        """
        Send WhatsApp message via Infobip API

        Args:
            phone_number: Target phone number
            message: Message content
            template_name: Optional WhatsApp template name

        Returns:
            Dict with API response details
        """
        try:
            import http.client

            # Parse base URL to get host
            from urllib.parse import urlparse
            parsed_url = urlparse(self.infobip_base_url)
            host = parsed_url.netloc

            # Create connection
            conn = http.client.HTTPSConnection(host)

            # Clean phone number
            clean_phone = phone_number.replace('+', '').replace('-', '').replace(' ', '')

            # Prepare payload based on template or text message
            if template_name:
                # Template message
                payload = json.dumps({
                    "messages": [
                        {
                            "from": self.infobip_from_number,
                            "to": clean_phone,
                            "content": {
                                "templateName": template_name,
                                "templateData": {
                                    "body": {
                                        "placeholders": [message]
                                    }
                                },
                                "language": "en"
                            }
                        }
                    ]
                })
                endpoint = "/whatsapp/1/message/template"
            else:
                # Text message
                payload = json.dumps({
                    "messages": [
                        {
                            "from": self.infobip_from_number,
                            "to": clean_phone,
                            "content": {
                                "text": message
                            }
                        }
                    ]
                })
                endpoint = "/whatsapp/1/message/text"

            # Prepare headers
            headers = {
                'Authorization': f'App {self.infobip_api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            # Send request
            conn.request("POST", endpoint, payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_data = json.loads(data.decode("utf-8"))

            conn.close()

            # Check response
            if res.status == 200:
                messages = response_data.get('messages', [])
                if messages:
                    return {
                        'success': True,
                        'provider': 'infobip_whatsapp',
                        'message_id': messages[0].get('messageId'),
                        'status': messages[0].get('status', {}).get('name'),
                        'response': response_data
                    }

            return {
                'success': False,
                'provider': 'infobip_whatsapp',
                'error': f"API returned status {res.status}",
                'response': response_data
            }

        except Exception as e:
            logger.error(f"Infobip WhatsApp error: {e}")
            return {
                'success': False,
                'provider': 'infobip_whatsapp',
                'error': str(e)
            }

    def send_sms_test(self, phone_number: str, message: str, test_name: str = "SMS Security Test") -> Dict:
        """
        Send SMS test message to authorized phone number

        Args:
            phone_number: Target phone number (must be authorized)
            message: Test message content
            test_name: Name of the test being conducted

        Returns:
            Dict with status and details
        """
        # Validate authorization
        if not self.validate_target_authorization(phone_number, 'phone'):
            result = {
                'success': False,
                'error': 'Target not authorized for testing',
                'target': phone_number,
                'test_name': test_name
            }
            self.log_test_activity('sms', phone_number, 'BLOCKED_UNAUTHORIZED', result)
            return result

        # Demo mode - simulate SMS sending
        if self.demo_mode:
            logger.info(f"[DEMO MODE] Would send SMS to {phone_number}: {message[:50]}...")
            result = {
                'success': True,
                'demo_mode': True,
                'target': phone_number,
                'message_length': len(message),
                'test_name': test_name,
                'sid': f"demo_sms_{datetime.utcnow().timestamp()}"
            }
            self.log_test_activity('sms', phone_number, 'DEMO_SUCCESS', result)
            return result

        # Real mode - send via configured provider (Infobip or TextBelt)
        try:
            if self.sms_provider == 'infobip' and self.infobip_api_key:
                # Use Infobip
                logger.info(f"Sending SMS via Infobip to {phone_number}")
                api_result = self._send_sms_via_infobip(phone_number, message)

                if api_result.get('success'):
                    result = {
                        'success': True,
                        'provider': 'infobip',
                        'target': phone_number,
                        'message_length': len(message),
                        'test_name': test_name,
                        'message_id': api_result.get('message_id'),
                        'status': api_result.get('status')
                    }
                    self.log_test_activity('sms', phone_number, 'SUCCESS', result)
                    logger.info(f"SMS sent via Infobip - Message ID: {result['message_id']}")
                    return result
                else:
                    raise ValueError(f"Infobip API error: {api_result.get('error')}")

            else:
                # Use TextBelt (fallback)
                import requests

                logger.info(f"Sending SMS via TextBelt to {phone_number}")

                # TextBelt API endpoint
                url = 'https://textbelt.com/text'

                # Prepare request data
                data = {
                    'phone': phone_number,
                    'message': message,
                    'key': self.textbelt_key  # Use 'textbelt' for free tier (1 msg/day) or paid API key
                }

                # Send SMS via TextBelt
                response = requests.post(url, data=data)
                response_data = response.json()

                if response_data.get('success'):
                    result = {
                        'success': True,
                        'provider': 'textbelt',
                        'target': phone_number,
                        'message_length': len(message),
                        'test_name': test_name,
                        'textId': response_data.get('textId'),
                        'quotaRemaining': response_data.get('quotaRemaining', 'N/A')
                    }
                    self.log_test_activity('sms', phone_number, 'SUCCESS', result)
                    logger.info(f"SMS sent via TextBelt - Quota remaining: {result['quotaRemaining']}")
                    return result
                else:
                    error_msg = response_data.get('error', 'Unknown error')
                    raise ValueError(f"TextBelt API error: {error_msg}")

        except Exception as e:
            logger.error(f"Error sending SMS test: {e}")
            result = {
                'success': False,
                'error': str(e),
                'target': phone_number,
                'test_name': test_name,
                'provider': self.sms_provider
            }
            self.log_test_activity('sms', phone_number, 'FAILED', result)
            return result

    def send_email_test(self, email_address: str, subject: str, message: str,
                       test_name: str = "Email Security Test") -> Dict:
        """
        Send email test message to authorized email address

        Args:
            email_address: Target email (must be authorized)
            subject: Email subject
            message: Email body content
            test_name: Name of the test being conducted

        Returns:
            Dict with status and details
        """
        # Validate authorization
        if not self.validate_target_authorization(email_address, 'email'):
            result = {
                'success': False,
                'error': 'Target not authorized for testing',
                'target': email_address,
                'test_name': test_name
            }
            self.log_test_activity('email', email_address, 'BLOCKED_UNAUTHORIZED', result)
            return result

        # Demo mode - simulate email sending
        if self.demo_mode:
            logger.info(f"[DEMO MODE] Would send email to {email_address}")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Body: {message[:100]}...")
            result = {
                'success': True,
                'demo_mode': True,
                'target': email_address,
                'subject': subject,
                'message_length': len(message),
                'test_name': test_name,
                'message_id': f"demo_email_{datetime.utcnow().timestamp()}"
            }
            self.log_test_activity('email', email_address, 'DEMO_SUCCESS', result)
            return result

        # Real mode - send via SendGrid
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            if not self.sendgrid_key:
                raise ValueError("SendGrid API key not configured")

            email_from = os.getenv('SENDGRID_FROM_EMAIL', 'security-testing@yourcompany.com')

            mail = Mail(
                from_email=email_from,
                to_emails=email_address,
                subject=subject,
                plain_text_content=message
            )

            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(mail)

            result = {
                'success': True,
                'target': email_address,
                'subject': subject,
                'message_length': len(message),
                'test_name': test_name,
                'status_code': response.status_code
            }
            self.log_test_activity('email', email_address, 'SUCCESS', result)
            return result

        except Exception as e:
            logger.error(f"Error sending email test: {e}")
            result = {
                'success': False,
                'error': str(e),
                'target': email_address,
                'test_name': test_name
            }
            self.log_test_activity('email', email_address, 'FAILED', result)
            return result

    def deploy_mobile_test(self, target: str, platform: str, test_type: str) -> Dict:
        """
        Deploy mobile security test to target device

        Args:
            target: Phone number or email of target device
            platform: 'ios' or 'android'
            test_type: Type of test to conduct

        Returns:
            Dict with test results
        """
        logger.info(f"Deploying mobile test: {test_type} on {platform} to {target}")

        # Detect target type
        target_type = self.detect_target_type(target)
        if not target_type:
            return {
                'success': False,
                'error': 'Invalid target format',
                'target': target
            }

        # Validate authorization
        if not self.validate_target_authorization(target, target_type):
            return {
                'success': False,
                'error': 'Target not authorized',
                'target': target
            }

        # Prepare test payload based on platform and test type
        test_config = self._get_test_config(platform, test_type)

        # Send test via appropriate channel
        if target_type == 'phone':
            result = self.send_sms_test(
                target,
                test_config['message'],
                test_name=f"{platform}_{test_type}"
            )
        elif target_type == 'email':
            result = self.send_email_test(
                target,
                test_config['subject'],
                test_config['message'],
                test_name=f"{platform}_{test_type}"
            )
        else:
            result = {
                'success': False,
                'error': 'Unsupported target type for mobile testing',
                'target': target
            }

        return result

    def _get_test_config(self, platform: str, test_type: str) -> Dict:
        """Get test configuration based on platform and test type"""

        configs = {
            'ios': {
                'phishing': {
                    'subject': 'Security Update Required',
                    'message': 'Your device requires a security update. Click here to update: [TEST LINK]'
                },
                'smishing': {
                    'message': 'Security Alert: Unusual activity detected on your account. Verify here: [TEST LINK]'
                }
            },
            'android': {
                'phishing': {
                    'subject': 'System Update Available',
                    'message': 'A critical system update is available for your device. Install now: [TEST LINK]'
                },
                'smishing': {
                    'message': 'Your package delivery failed. Reschedule here: [TEST LINK]'
                }
            }
        }

        return configs.get(platform, {}).get(test_type, {
            'subject': f'{platform.upper()} Security Test',
            'message': 'This is a security testing message from your IT security team.'
        })

    def get_test_statistics(self) -> Dict:
        """Get statistics on mobile security tests"""
        try:
            from sqlalchemy import func, text

            # Query test statistics
            total_tests = self.session.query(func.count(AttackSimulation.id)).filter(
                AttackSimulation.attack_type.like('mobile_testing_%')
            ).scalar()

            successful_tests = self.session.query(func.count(AttackSimulation.id)).filter(
                AttackSimulation.attack_type.like('mobile_testing_%'),
                AttackSimulation.status == 'SUCCESS'
            ).scalar()

            return {
                'total_tests': total_tests or 0,
                'successful_tests': successful_tests or 0,
                'success_rate': (successful_tests / total_tests * 100) if total_tests else 0,
                'authorized_targets': len(self.authorized_targets)
            }

        except Exception as e:
            logger.error(f"Error getting test statistics: {e}")
            return {
                'total_tests': 0,
                'successful_tests': 0,
                'success_rate': 0,
                'authorized_targets': len(self.authorized_targets)
            }

    def send_whatsapp_test(self, phone_number: str, message: str,
                          test_name: str = "WhatsApp Security Test",
                          template_name: str = None) -> Dict:
        """
        Send WhatsApp test message to authorized phone number via Infobip

        Args:
            phone_number: Target phone number (must be authorized)
            message: Test message content
            test_name: Name of the test being conducted
            template_name: Optional WhatsApp template name (for template messages)

        Returns:
            Dict with status and details
        """
        # Check if WhatsApp is enabled
        if not self.infobip_whatsapp_enabled or not self.infobip_api_key:
            return {
                'success': False,
                'error': 'WhatsApp testing not enabled or Infobip not configured',
                'target': phone_number,
                'test_name': test_name
            }

        # Validate authorization
        if not self.validate_target_authorization(phone_number, 'phone'):
            result = {
                'success': False,
                'error': 'Target not authorized for testing',
                'target': phone_number,
                'test_name': test_name
            }
            self.log_test_activity('whatsapp', phone_number, 'BLOCKED_UNAUTHORIZED', result)
            return result

        # Demo mode - simulate WhatsApp sending
        if self.demo_mode:
            logger.info(f"[DEMO MODE] Would send WhatsApp to {phone_number}: {message[:50]}...")
            result = {
                'success': True,
                'demo_mode': True,
                'provider': 'infobip_whatsapp',
                'target': phone_number,
                'message_length': len(message),
                'test_name': test_name,
                'message_id': f"demo_whatsapp_{datetime.utcnow().timestamp()}"
            }
            self.log_test_activity('whatsapp', phone_number, 'DEMO_SUCCESS', result)
            return result

        # Real mode - send via Infobip WhatsApp
        try:
            logger.info(f"Sending WhatsApp via Infobip to {phone_number}")
            api_result = self._send_whatsapp_via_infobip(phone_number, message, template_name)

            if api_result.get('success'):
                result = {
                    'success': True,
                    'provider': 'infobip_whatsapp',
                    'target': phone_number,
                    'message_length': len(message),
                    'test_name': test_name,
                    'message_id': api_result.get('message_id'),
                    'status': api_result.get('status'),
                    'template': template_name
                }
                self.log_test_activity('whatsapp', phone_number, 'SUCCESS', result)
                logger.info(f"WhatsApp sent via Infobip - Message ID: {result['message_id']}")
                return result
            else:
                raise ValueError(f"Infobip WhatsApp API error: {api_result.get('error')}")

        except Exception as e:
            logger.error(f"Error sending WhatsApp test: {e}")
            result = {
                'success': False,
                'error': str(e),
                'target': phone_number,
                'test_name': test_name,
                'provider': 'infobip_whatsapp'
            }
            self.log_test_activity('whatsapp', phone_number, 'FAILED', result)
            return result

    def __del__(self):
        """Cleanup database session"""
        try:
            self.session.close()
        except:
            pass


def render():
    """Render module information"""
    return "Mobile Security Testing Module: iOS and Android penetration testing framework"
