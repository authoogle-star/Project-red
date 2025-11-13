#!/usr/bin/env python3
"""
Steganography Injection Module
Embeds mobile exploit payloads into images, URLs, and files for covert delivery
Blue Team monitoring detects and analyzes steganographic content
"""

import os
import base64
import logging
from PIL import Image
from io import BytesIO
from typing import Dict, Optional, Tuple
import struct

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SteganographyInjector:
    """
    Steganography module for covert payload delivery
    Supports image LSB injection, URL encoding, and file embedding
    """

    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp']
        logger.info("Steganography Injector initialized")

    # ================== IMAGE STEGANOGRAPHY ==================

    def embed_payload_in_image(self, image_path: str, payload: str, output_path: str) -> Dict:
        """
        Embed exploit payload into image using LSB (Least Significant Bit) steganography

        Args:
            image_path: Path to original image
            payload: Exploit payload to embed
            output_path: Path to save steganographic image

        Returns:
            Dict with embedding status and details
        """
        try:
            logger.info(f"[STEGO] Embedding payload into image: {image_path}")

            # Open image
            img = Image.open(image_path)

            # Convert to RGB if not already
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Encode payload
            encoded_payload = payload.encode('utf-8')
            payload_length = len(encoded_payload)

            # Add length header (4 bytes)
            header = struct.pack('>I', payload_length)
            full_data = header + encoded_payload

            # Convert to binary
            binary_data = ''.join(format(byte, '08b') for byte in full_data)

            # Check if image can hold the payload
            img_data = list(img.getdata())
            max_bytes = len(img_data) * 3 // 8  # 3 color channels, 1 bit per channel

            if len(full_data) > max_bytes:
                return {
                    'success': False,
                    'error': 'Payload too large for image',
                    'payload_size': len(full_data),
                    'max_size': max_bytes
                }

            # Embed data using LSB
            data_index = 0
            new_img_data = []

            for pixel in img_data:
                if data_index < len(binary_data):
                    # Modify RGB channels
                    r, g, b = pixel

                    if data_index < len(binary_data):
                        r = (r & 0xFE) | int(binary_data[data_index])
                        data_index += 1

                    if data_index < len(binary_data):
                        g = (g & 0xFE) | int(binary_data[data_index])
                        data_index += 1

                    if data_index < len(binary_data):
                        b = (b & 0xFE) | int(binary_data[data_index])
                        data_index += 1

                    new_img_data.append((r, g, b))
                else:
                    new_img_data.append(pixel)

            # Create new image with embedded data
            stego_img = Image.new(img.mode, img.size)
            stego_img.putdata(new_img_data)
            stego_img.save(output_path)

            logger.info(f"[STEGO] Payload successfully embedded: {output_path}")

            return {
                'success': True,
                'original_image': image_path,
                'stego_image': output_path,
                'payload_size': payload_length,
                'embedding_method': 'LSB',
                'detection_difficulty': 'HIGH'
            }

        except Exception as e:
            logger.error(f"[STEGO] Image embedding error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def extract_payload_from_image(self, stego_image_path: str) -> Dict:
        """
        Extract hidden payload from steganographic image
        Used by Blue Team for analysis

        Args:
            stego_image_path: Path to steganographic image

        Returns:
            Dict with extracted payload and analysis
        """
        try:
            logger.info(f"[BLUE TEAM] Analyzing image for steganographic content: {stego_image_path}")

            # Open image
            img = Image.open(stego_image_path)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Extract LSB data
            img_data = list(img.getdata())
            binary_data = ''

            for pixel in img_data:
                r, g, b = pixel
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

            # Extract length header (first 32 bits)
            length_bits = binary_data[:32]
            payload_length = struct.unpack('>I', int(length_bits, 2).to_bytes(4, 'big'))[0]

            # Extract payload
            payload_bits = binary_data[32:32 + (payload_length * 8)]
            payload_bytes = bytearray()

            for i in range(0, len(payload_bits), 8):
                byte = payload_bits[i:i+8]
                if len(byte) == 8:
                    payload_bytes.append(int(byte, 2))

            payload = payload_bytes.decode('utf-8', errors='ignore')

            # Analyze payload for malicious patterns
            threat_indicators = self._analyze_payload(payload)

            logger.info(f"[BLUE TEAM] Steganographic payload extracted and analyzed")

            return {
                'success': True,
                'payload': payload,
                'payload_length': payload_length,
                'threat_level': threat_indicators['threat_level'],
                'indicators': threat_indicators['indicators'],
                'malicious_patterns': threat_indicators['patterns']
            }

        except Exception as e:
            logger.error(f"[BLUE TEAM] Extraction error: {e}")
            return {
                'success': False,
                'error': str(e),
                'analysis': 'Could not extract payload - may not contain steganographic data'
            }

    # ================== URL STEGANOGRAPHY ==================

    def embed_payload_in_url(self, base_url: str, payload: str) -> Dict:
        """
        Embed exploit payload in URL using various encoding techniques

        Args:
            base_url: Base URL for encoding
            payload: Exploit payload

        Returns:
            Dict with encoded URL
        """
        try:
            logger.info(f"[STEGO] Embedding payload in URL")

            # Base64 encode payload
            encoded_payload = base64.b64encode(payload.encode()).decode()

            # Create steganographic URL with multiple encoding layers
            # Layer 1: URL parameter encoding
            stego_url = f"{base_url}?token={encoded_payload}"

            # Layer 2: Add decoy parameters
            stego_url += f"&utm_source=email&utm_campaign=security_update&ref=mobile"

            # Layer 3: Fragment identifier (often ignored by servers)
            stego_url += f"#{base64.b64encode(b'exploit').decode()}"

            logger.info(f"[STEGO] URL encoding complete")

            return {
                'success': True,
                'stego_url': stego_url,
                'base_url': base_url,
                'encoding_layers': 3,
                'payload_location': 'token parameter',
                'detection_difficulty': 'MEDIUM'
            }

        except Exception as e:
            logger.error(f"[STEGO] URL encoding error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def extract_payload_from_url(self, stego_url: str) -> Dict:
        """
        Extract hidden payload from steganographic URL
        Used by Blue Team

        Args:
            stego_url: Steganographic URL

        Returns:
            Dict with extracted payload
        """
        try:
            logger.info(f"[BLUE TEAM] Analyzing URL for hidden payload")

            from urllib.parse import urlparse, parse_qs

            # Parse URL
            parsed = urlparse(stego_url)
            params = parse_qs(parsed.query)

            # Extract token parameter
            if 'token' in params:
                encoded_payload = params['token'][0]
                payload = base64.b64decode(encoded_payload).decode('utf-8', errors='ignore')

                # Analyze payload
                threat_indicators = self._analyze_payload(payload)

                return {
                    'success': True,
                    'payload': payload,
                    'extraction_method': 'URL parameter decode',
                    'threat_level': threat_indicators['threat_level'],
                    'indicators': threat_indicators['indicators']
                }
            else:
                return {
                    'success': False,
                    'error': 'No encoded payload found in URL'
                }

        except Exception as e:
            logger.error(f"[BLUE TEAM] URL extraction error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # ================== FILE STEGANOGRAPHY ==================

    def embed_payload_in_file(self, file_path: str, payload: str, output_path: str) -> Dict:
        """
        Embed exploit payload into file (PDF, DOCX, etc.)

        Args:
            file_path: Original file path
            payload: Exploit payload
            output_path: Output path for steganographic file

        Returns:
            Dict with embedding status
        """
        try:
            logger.info(f"[STEGO] Embedding payload in file: {file_path}")

            # Read original file
            with open(file_path, 'rb') as f:
                original_data = f.read()

            # Encode payload
            encoded_payload = payload.encode('utf-8')

            # Create marker for payload location
            marker = b'<STEGO_PAYLOAD>'
            end_marker = b'</STEGO_PAYLOAD>'

            # Append payload to end of file (most file formats ignore trailing data)
            stego_data = original_data + marker + encoded_payload + end_marker

            # Write steganographic file
            with open(output_path, 'wb') as f:
                f.write(stego_data)

            logger.info(f"[STEGO] File embedding complete: {output_path}")

            return {
                'success': True,
                'original_file': file_path,
                'stego_file': output_path,
                'payload_size': len(encoded_payload),
                'file_size_increase': len(stego_data) - len(original_data),
                'detection_difficulty': 'LOW-MEDIUM'
            }

        except Exception as e:
            logger.error(f"[STEGO] File embedding error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def extract_payload_from_file(self, stego_file_path: str) -> Dict:
        """
        Extract hidden payload from steganographic file
        Used by Blue Team

        Args:
            stego_file_path: Steganographic file path

        Returns:
            Dict with extracted payload
        """
        try:
            logger.info(f"[BLUE TEAM] Analyzing file for hidden payload: {stego_file_path}")

            # Read file
            with open(stego_file_path, 'rb') as f:
                file_data = f.read()

            # Look for payload markers
            marker = b'<STEGO_PAYLOAD>'
            end_marker = b'</STEGO_PAYLOAD>'

            start_idx = file_data.find(marker)

            if start_idx != -1:
                start_idx += len(marker)
                end_idx = file_data.find(end_marker, start_idx)

                if end_idx != -1:
                    payload_bytes = file_data[start_idx:end_idx]
                    payload = payload_bytes.decode('utf-8', errors='ignore')

                    # Analyze payload
                    threat_indicators = self._analyze_payload(payload)

                    logger.info(f"[BLUE TEAM] File payload extracted and analyzed")

                    return {
                        'success': True,
                        'payload': payload,
                        'payload_location': f'bytes {start_idx} to {end_idx}',
                        'threat_level': threat_indicators['threat_level'],
                        'indicators': threat_indicators['indicators'],
                        'file_path': stego_file_path
                    }

            return {
                'success': False,
                'error': 'No steganographic payload found in file'
            }

        except Exception as e:
            logger.error(f"[BLUE TEAM] File extraction error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # ================== BLUE TEAM ANALYSIS ==================

    def _analyze_payload(self, payload: str) -> Dict:
        """
        Analyze extracted payload for malicious patterns
        Used by Blue Team threat detection

        Args:
            payload: Extracted payload string

        Returns:
            Dict with threat analysis
        """
        indicators = []
        patterns_found = []
        threat_level = 'LOW'

        # Check for common malicious patterns
        malicious_patterns = {
            'reverse_shell': ['/dev/tcp/', 'bash -i', 'nc -e', 'socket.socket'],
            'code_execution': ['subprocess.', 'os.system', 'eval(', 'exec(', 'Invoke-Expression'],
            'privilege_escalation': ['sudo ', 'NOPASSWD', 'SUID', 'chmod +s'],
            'data_exfiltration': ['curl ', 'wget ', 'requests.post', 'ftp'],
            'persistence': ['cron', 'LaunchDaemon', 'schtasks', 'startup'],
            'c2_callback': ['zeroclickexploits.ddns.net', 'C2', 'beacon']
        }

        for pattern_type, pattern_list in malicious_patterns.items():
            for pattern in pattern_list:
                if pattern.lower() in payload.lower():
                    indicators.append(pattern_type)
                    patterns_found.append(pattern)
                    threat_level = 'HIGH'

        # Check for exploit CVEs
        cve_patterns = ['CVE-2021-30860', 'CVE-2023-45866', 'CVE-2022']
        for cve in cve_patterns:
            if cve in payload:
                indicators.append('known_exploit')
                patterns_found.append(cve)
                threat_level = 'CRITICAL'

        # Check for encoded/obfuscated content
        if 'base64' in payload.lower() or len([c for c in payload if c.isalnum()]) > len(payload) * 0.8:
            indicators.append('obfuscation')
            if threat_level == 'LOW':
                threat_level = 'MEDIUM'

        return {
            'threat_level': threat_level,
            'indicators': list(set(indicators)),
            'patterns': patterns_found,
            'analysis_complete': True
        }

    # ================== UTILITY METHODS ==================

    def generate_innocent_looking_image(self, width: int = 800, height: int = 600, output_path: str = None) -> str:
        """
        Generate innocent-looking image for payload embedding

        Args:
            width: Image width
            height: Image height
            output_path: Optional output path

        Returns:
            Path to generated image
        """
        if output_path is None:
            output_path = 'tmp/innocent_image.png'

        os.makedirs('tmp', exist_ok=True)

        # Create simple gradient image
        img = Image.new('RGB', (width, height))
        pixels = []

        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = 128
                pixels.append((r, g, b))

        img.putdata(pixels)
        img.save(output_path)

        logger.info(f"[STEGO] Generated innocent-looking image: {output_path}")
        return output_path


def render():
    """Module render function"""
    return "Steganography Injector: Covert payload embedding in images, URLs, and files"
