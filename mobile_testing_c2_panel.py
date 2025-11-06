#!/usr/bin/env python3
"""
Mobile Testing Command & Control Panel
Flask web interface for mobile security testing operations
Based on mobile-click-testing.txt architecture
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import os
import re
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from modules.mobile_security_testing import MobileSecurityTesting

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mobile_c2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize mobile testing module
mobile_tester = MobileSecurityTesting()

# HTML Template for C2 Panel
C2_PANEL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Testing C2 Panel - Project Red Sword</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }
        .header {
            text-align: center;
            border: 2px solid #00ff00;
            padding: 20px;
            margin-bottom: 30px;
            background: #1a1a1a;
        }
        .header h1 {
            color: #ff0000;
            text-shadow: 0 0 10px #ff0000;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .section {
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 20px;
            margin-bottom: 20px;
        }
        .section h2 {
            color: #00ff00;
            margin-bottom: 15px;
            border-bottom: 1px solid #00ff00;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #00ff00;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            background: #0a0a0a;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }
        button {
            background: #ff0000;
            color: #ffffff;
            border: none;
            padding: 12px 30px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            margin-right: 10px;
            transition: all 0.3s;
        }
        button:hover {
            background: #cc0000;
            box-shadow: 0 0 10px #ff0000;
        }
        button.secondary {
            background: #00ff00;
            color: #000000;
        }
        button.secondary:hover {
            background: #00cc00;
            box-shadow: 0 0 10px #00ff00;
        }
        .status {
            padding: 15px;
            margin-top: 15px;
            border: 1px solid #00ff00;
            background: #0a0a0a;
            display: none;
        }
        .status.success {
            border-color: #00ff00;
            color: #00ff00;
        }
        .status.error {
            border-color: #ff0000;
            color: #ff0000;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-box {
            background: #0a0a0a;
            padding: 15px;
            border: 1px solid #00ff00;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            color: #ff0000;
            font-weight: bold;
        }
        .stat-label {
            color: #00ff00;
            margin-top: 5px;
        }
        .warning {
            background: #1a0000;
            border: 2px solid #ff0000;
            padding: 15px;
            margin-bottom: 20px;
            color: #ff0000;
        }
        .log-output {
            background: #0a0a0a;
            border: 1px solid #00ff00;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 PROJECT RED SWORD</h1>
            <h2>Mobile Testing Command & Control Panel</h2>
            <p>In-House Team Security Testing | iOS & Android</p>
        </div>

        <div class="warning">
            <strong>⚠️ AUTHORIZED TESTING ONLY ⚠️</strong><br>
            This system is for authorized in-house security team testing only.<br>
            All activities are logged and audited. Only authorized targets can be tested.
        </div>

        <!-- Statistics Dashboard -->
        <div class="section">
            <h2>📊 Testing Statistics</h2>
            <div class="stats-grid" id="stats">
                <div class="stat-box">
                    <div class="stat-value" id="stat-total">-</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-success">-</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-rate">-</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-targets">-</div>
                    <div class="stat-label">Auth Targets</div>
                </div>
            </div>
        </div>

        <!-- SMS Testing Section -->
        <div class="section">
            <h2>📱 SMS Security Testing</h2>
            <form id="smsForm">
                <div class="form-group">
                    <label for="sms-phone">Target Phone Number (must be authorized):</label>
                    <input type="text" id="sms-phone" placeholder="+1234567890" required>
                </div>
                <div class="form-group">
                    <label for="sms-test-type">Test Type:</label>
                    <select id="sms-test-type">
                        <option value="phishing">Phishing/Smishing Test</option>
                        <option value="malware">Malware Link Test</option>
                        <option value="social">Social Engineering Test</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="sms-message">Test Message:</label>
                    <textarea id="sms-message" rows="3" placeholder="Your package delivery failed. Click to reschedule: [TEST_LINK]"></textarea>
                </div>
                <button type="submit">🚀 Send SMS Test</button>
                <button type="button" class="secondary" onclick="clearForm('smsForm')">Clear</button>
            </form>
            <div class="status" id="sms-status"></div>
        </div>

        <!-- Email Testing Section -->
        <div class="section">
            <h2>📧 Email Security Testing</h2>
            <form id="emailForm">
                <div class="form-group">
                    <label for="email-address">Target Email (must be authorized):</label>
                    <input type="email" id="email-address" placeholder="test@yourcompany.com" required>
                </div>
                <div class="form-group">
                    <label for="email-platform">Platform:</label>
                    <select id="email-platform">
                        <option value="ios">iOS</option>
                        <option value="android">Android</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="email-test-type">Test Type:</label>
                    <select id="email-test-type">
                        <option value="phishing">Phishing Email</option>
                        <option value="malicious-attachment">Malicious Attachment</option>
                        <option value="credential-harvest">Credential Harvesting</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="email-subject">Subject:</label>
                    <input type="text" id="email-subject" placeholder="Security Update Required" required>
                </div>
                <div class="form-group">
                    <label for="email-message">Email Body:</label>
                    <textarea id="email-message" rows="5" placeholder="Your device requires a security update..."></textarea>
                </div>
                <button type="submit">🚀 Send Email Test</button>
                <button type="button" class="secondary" onclick="clearForm('emailForm')">Clear</button>
            </form>
            <div class="status" id="email-status"></div>
        </div>

        <!-- Mobile Deployment Section -->
        <div class="section">
            <h2>📲 Mobile Test Deployment</h2>
            <form id="deployForm">
                <div class="form-group">
                    <label for="deploy-target">Target (Phone or Email):</label>
                    <input type="text" id="deploy-target" placeholder="+1234567890 or email@company.com" required>
                </div>
                <div class="form-group">
                    <label for="deploy-platform">Platform:</label>
                    <select id="deploy-platform">
                        <option value="ios">iOS</option>
                        <option value="android">Android</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="deploy-test-type">Test Type:</label>
                    <select id="deploy-test-type">
                        <option value="phishing">Phishing</option>
                        <option value="smishing">Smishing</option>
                        <option value="malicious_profile">Malicious Profile (iOS)</option>
                        <option value="malicious_apk">Malicious APK (Android)</option>
                    </select>
                </div>
                <button type="submit">🎯 Deploy Test</button>
                <button type="button" class="secondary" onclick="clearForm('deployForm')">Clear</button>
            </form>
            <div class="status" id="deploy-status"></div>
        </div>

        <!-- Activity Log -->
        <div class="section">
            <h2>📝 Activity Log</h2>
            <div class="log-output" id="log-output">
                <div>[System] Mobile Testing C2 Panel initialized</div>
                <div>[System] Waiting for operator commands...</div>
            </div>
        </div>
    </div>

    <script>
        // Load statistics on page load
        window.addEventListener('load', loadStatistics);

        // Refresh stats every 10 seconds
        setInterval(loadStatistics, 10000);

        function loadStatistics() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('stat-total').textContent = data.total_tests;
                    document.getElementById('stat-success').textContent = data.successful_tests;
                    document.getElementById('stat-rate').textContent = data.success_rate.toFixed(1) + '%';
                    document.getElementById('stat-targets').textContent = data.authorized_targets;
                })
                .catch(error => console.error('Error loading stats:', error));
        }

        function logActivity(message, type = 'info') {
            const logOutput = document.getElementById('log-output');
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? '#ff0000' : type === 'success' ? '#00ff00' : '#ffff00';
            const entry = document.createElement('div');
            entry.style.color = color;
            entry.textContent = `[${timestamp}] ${message}`;
            logOutput.appendChild(entry);
            logOutput.scrollTop = logOutput.scrollHeight;
        }

        function showStatus(elementId, message, isSuccess) {
            const status = document.getElementById(elementId);
            status.textContent = message;
            status.className = 'status ' + (isSuccess ? 'success' : 'error');
            status.style.display = 'block';
            setTimeout(() => {
                status.style.display = 'none';
            }, 5000);
        }

        function clearForm(formId) {
            document.getElementById(formId).reset();
        }

        // SMS Form Handler
        document.getElementById('smsForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const phone = document.getElementById('sms-phone').value;
            const testType = document.getElementById('sms-test-type').value;
            const message = document.getElementById('sms-message').value;

            logActivity(`Initiating SMS test to ${phone}`, 'info');

            fetch('/api/sms', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone_number: phone,
                    test_name: testType,
                    message: message
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('sms-status', '✓ SMS test sent successfully!', true);
                    logActivity(`SMS test sent to ${phone} - ${data.demo_mode ? '[DEMO MODE]' : 'REAL'}`, 'success');
                    loadStatistics();
                } else {
                    showStatus('sms-status', '✗ Failed: ' + data.error, false);
                    logActivity(`SMS test failed: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('sms-status', '✗ Error: ' + error, false);
                logActivity(`SMS test error: ${error}`, 'error');
            });
        });

        // Email Form Handler
        document.getElementById('emailForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email-address').value;
            const platform = document.getElementById('email-platform').value;
            const testType = document.getElementById('email-test-type').value;
            const subject = document.getElementById('email-subject').value;
            const message = document.getElementById('email-message').value;

            logActivity(`Initiating email test to ${email}`, 'info');

            fetch('/api/email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email_address: email,
                    platform: platform,
                    test_name: testType,
                    subject: subject,
                    message: message
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('email-status', '✓ Email test sent successfully!', true);
                    logActivity(`Email test sent to ${email} - ${data.demo_mode ? '[DEMO MODE]' : 'REAL'}`, 'success');
                    loadStatistics();
                } else {
                    showStatus('email-status', '✗ Failed: ' + data.error, false);
                    logActivity(`Email test failed: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('email-status', '✗ Error: ' + error, false);
                logActivity(`Email test error: ${error}`, 'error');
            });
        });

        // Deploy Form Handler
        document.getElementById('deployForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const target = document.getElementById('deploy-target').value;
            const platform = document.getElementById('deploy-platform').value;
            const testType = document.getElementById('deploy-test-type').value;

            logActivity(`Deploying ${platform} test (${testType}) to ${target}`, 'info');

            fetch('/api/deploy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target: target,
                    platform: platform,
                    test_type: testType
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('deploy-status', '✓ Test deployed successfully!', true);
                    logActivity(`Test deployed to ${target} - ${data.demo_mode ? '[DEMO MODE]' : 'REAL'}`, 'success');
                    loadStatistics();
                } else {
                    showStatus('deploy-status', '✗ Failed: ' + data.error, false);
                    logActivity(`Deployment failed: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('deploy-status', '✗ Error: ' + error, false);
                logActivity(`Deployment error: ${error}`, 'error');
            });
        });
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Main C2 panel interface"""
    return render_template_string(C2_PANEL_HTML)


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get mobile testing statistics"""
    try:
        stats = mobile_tester.get_test_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sms', methods=['POST'])
def send_sms():
    """Send SMS security test"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message', 'Security test message')
        test_name = data.get('test_name', 'SMS Test')

        logger.info(f"SMS test request: {phone_number} - {test_name}")

        result = mobile_tester.send_sms_test(phone_number, message, test_name)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in SMS endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/email', methods=['POST'])
def send_email():
    """Send email security test"""
    try:
        data = request.get_json()
        email_address = data.get('email_address')
        subject = data.get('subject', 'Security Test')
        message = data.get('message', 'Security test email')
        test_name = data.get('test_name', 'Email Test')

        logger.info(f"Email test request: {email_address} - {test_name}")

        result = mobile_tester.send_email_test(email_address, subject, message, test_name)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in email endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/deploy', methods=['POST'])
def deploy_test():
    """Deploy mobile security test"""
    try:
        data = request.get_json()
        target = data.get('target')
        platform = data.get('platform', 'ios')
        test_type = data.get('test_type', 'phishing')

        logger.info(f"Deploy test request: {target} - {platform} - {test_type}")

        result = mobile_tester.deploy_mobile_test(target, platform, test_type)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in deploy endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/whatsapp', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp security test"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message', 'Security test message')
        test_name = data.get('test_name', 'WhatsApp Test')
        template_name = data.get('template_name')

        logger.info(f"WhatsApp test request: {phone_number} - {test_name}")

        result = mobile_tester.send_whatsapp_test(phone_number, message, test_name, template_name)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in WhatsApp endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'demo_mode': mobile_tester.demo_mode,
        'sms_provider': mobile_tester.sms_provider,
        'whatsapp_enabled': mobile_tester.infobip_whatsapp_enabled
    })


if __name__ == '__main__':
    logger.info("="*70)
    logger.info("Mobile Testing C2 Panel Starting")
    logger.info("="*70)
    logger.info(f"Demo Mode: {mobile_tester.demo_mode}")
    logger.info(f"Authorized Targets: {len(mobile_tester.authorized_targets)}")
    logger.info("Access panel at: http://localhost:5007")
    logger.info("="*70)

    app.run(
        host='0.0.0.0',
        port=5007,
        debug=False
    )
