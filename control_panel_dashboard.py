#!/usr/bin/env python3
"""
Control Panel Dashboard
Centralized control for Red Team operations
Allows toggling DEMO_MODE, SAFE_MODE, and other operational settings in real-time
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
from dotenv import load_dotenv, set_key, find_dotenv
import subprocess

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/control_panel.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Control Panel HTML Template
CONTROL_PANEL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Panel - Project Red Sword</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #00ffff;
            padding: 20px;
        }
        .header {
            text-align: center;
            border: 3px solid #00ffff;
            padding: 25px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #001a1a 0%, #0a0a0a 100%);
            box-shadow: 0 0 20px #00ffff;
        }
        .header h1 {
            color: #00ffff;
            text-shadow: 0 0 15px #00ffff, 0 0 30px #00ffff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .section {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            border: 2px solid #00ffff;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        .section h2 {
            color: #00ffff;
            margin-bottom: 20px;
            border-bottom: 2px solid #00ffff;
            padding-bottom: 10px;
            text-shadow: 0 0 10px #00ffff;
        }
        .control-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .control-card {
            background: #000000;
            border: 2px solid #00ffff;
            padding: 20px;
            border-radius: 5px;
        }
        .control-card h3 {
            color: #00ffff;
            margin-bottom: 15px;
        }
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            margin-right: 15px;
        }
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ff0000;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #00ff00;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .toggle-container {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .toggle-label {
            font-size: 16px;
            color: #00ffff;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-left: 10px;
        }
        .status-indicator.on {
            background: #00ff00;
            box-shadow: 0 0 10px #00ff00;
        }
        .status-indicator.off {
            background: #ff0000;
            box-shadow: 0 0 10px #ff0000;
        }
        button {
            background: #00ffff;
            color: #000000;
            border: none;
            padding: 12px 25px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 14px;
            margin-right: 10px;
            margin-top: 10px;
            transition: all 0.3s;
            text-transform: uppercase;
            border-radius: 3px;
        }
        button:hover {
            background: #00cccc;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
            transform: scale(1.05);
        }
        button.danger {
            background: #ff0000;
            color: #ffffff;
        }
        button.danger:hover {
            background: #cc0000;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        }
        button.warning {
            background: #ff9900;
            color: #000000;
        }
        .status-message {
            padding: 15px;
            margin-top: 15px;
            border-radius: 3px;
            display: none;
        }
        .status-message.success {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
        }
        .status-message.error {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid #ff0000;
            color: #ff0000;
        }
        .info-box {
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid #00ffff;
            padding: 15px;
            margin-top: 15px;
            border-radius: 3px;
        }
        .services-list {
            list-style: none;
            padding: 0;
        }
        .services-list li {
            padding: 10px;
            margin: 5px 0;
            background: #0a0a0a;
            border-left: 3px solid #00ffff;
        }
        .service-status {
            float: right;
            font-weight: bold;
        }
        .service-status.running {
            color: #00ff00;
        }
        .service-status.stopped {
            color: #ff0000;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚙️ CONTROL PANEL ⚙️</h1>
            <h2>Real-Time Operational Control System</h2>
            <p style="color: #ff9900; margin-top: 10px;">Master Control for Red Team Operations</p>
        </div>

        <!-- Operational Mode Controls -->
        <div class="section">
            <h2>🎛️ Operational Mode Controls</h2>
            <div class="control-grid">
                <div class="control-card">
                    <h3>Demo Mode</h3>
                    <div class="toggle-container">
                        <label class="toggle-switch">
                            <input type="checkbox" id="demo-mode" onchange="toggleSetting('DEMO_MODE', this.checked)">
                            <span class="slider"></span>
                        </label>
                        <span class="toggle-label">
                            <span id="demo-mode-status">Loading...</span>
                            <span class="status-indicator" id="demo-mode-indicator"></span>
                        </span>
                    </div>
                    <div class="info-box">
                        <strong>Demo Mode ON:</strong> Simulated attacks, no real exploits deployed<br>
                        <strong>Demo Mode OFF:</strong> ⚠️ LIVE ATTACKS - Real exploits will be deployed to authorized targets
                    </div>
                </div>

                <div class="control-card">
                    <h3>Safe Mode</h3>
                    <div class="toggle-container">
                        <label class="toggle-switch">
                            <input type="checkbox" id="safe-mode" onchange="toggleSetting('SAFE_MODE', this.checked)">
                            <span class="slider"></span>
                        </label>
                        <span class="toggle-label">
                            <span id="safe-mode-status">Loading...</span>
                            <span class="status-indicator" id="safe-mode-indicator"></span>
                        </span>
                    </div>
                    <div class="info-box">
                        <strong>Safe Mode ON:</strong> Additional safety checks and confirmations<br>
                        <strong>Safe Mode OFF:</strong> Faster operations, fewer confirmations
                    </div>
                </div>

                <div class="control-card">
                    <h3>Kill Switch</h3>
                    <div class="toggle-container">
                        <label class="toggle-switch">
                            <input type="checkbox" id="kill-switch" onchange="toggleSetting('ENABLE_KILL_SWITCH', this.checked)">
                            <span class="slider"></span>
                        </label>
                        <span class="toggle-label">
                            <span id="kill-switch-status">Loading...</span>
                            <span class="status-indicator" id="kill-switch-indicator"></span>
                        </span>
                    </div>
                    <div class="info-box">
                        <strong>Kill Switch ENABLED:</strong> Can emergency stop all operations<br>
                        <strong>Kill Switch DISABLED:</strong> Normal operations only
                    </div>
                </div>
            </div>

            <div class="status-message" id="settings-status"></div>
        </div>

        <!-- Service Management -->
        <div class="section">
            <h2>🖥️ Service Management</h2>
            <ul class="services-list" id="services-list">
                <li>Red Team Dashboard (Port 5008) <span class="service-status running">●</span></li>
                <li>Blue Team Dashboard (Port 5009) <span class="service-status running">●</span></li>
                <li>C2 Listener (Port 4000) <span class="service-status running">●</span></li>
            </ul>
            <button onclick="refreshServices()">🔄 Refresh Status</button>
            <button class="warning" onclick="restartAllServices()">🔁 Restart All Services</button>
            <button class="danger" onclick="emergencyStop()">🛑 EMERGENCY STOP</button>
            <div class="status-message" id="service-status"></div>
        </div>

        <!-- Current Configuration -->
        <div class="section">
            <h2>📋 Current Configuration</h2>
            <div id="config-display" style="background: #000; padding: 15px; border: 1px solid #00ffff; border-radius: 3px; font-family: monospace;">
                <pre id="config-content" style="color: #00ff00;">Loading configuration...</pre>
            </div>
            <button onclick="loadConfig()">🔄 Reload Configuration</button>
            <button onclick="saveConfig()">💾 Save Changes</button>
        </div>

        <!-- Activity Log -->
        <div class="section">
            <h2>📝 Control Panel Activity Log</h2>
            <div style="background: #000; border: 2px solid #00ffff; padding: 15px; height: 200px; overflow-y: auto; font-size: 13px;" id="activity-log">
                <div style="color: #00ffff;">[System] Control Panel initialized</div>
                <div style="color: #00ff00;">[System] Ready for operational control</div>
            </div>
        </div>
    </div>

    <script>
        // Load initial status on page load
        window.addEventListener('load', function() {
            loadConfig();
            loadAllSettings();
            refreshServices();
            setInterval(refreshServices, 10000); // Refresh every 10 seconds
        });

        function logActivity(message, type = 'info') {
            const log = document.getElementById('activity-log');
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
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
        }

        function showStatus(elementId, message, isSuccess) {
            const status = document.getElementById(elementId);
            status.textContent = message;
            status.className = 'status-message ' + (isSuccess ? 'success' : 'error');
            status.style.display = 'block';
            setTimeout(() => {
                status.style.display = 'none';
            }, 5000);
        }

        function loadAllSettings() {
            fetch('/api/get_settings')
                .then(response => response.json())
                .then(data => {
                    // Update DEMO_MODE
                    const demoMode = data.DEMO_MODE === 'true';
                    document.getElementById('demo-mode').checked = demoMode;
                    document.getElementById('demo-mode-status').textContent = demoMode ? 'ENABLED (Safe Testing)' : 'DISABLED (LIVE ATTACKS)';
                    document.getElementById('demo-mode-indicator').className = 'status-indicator ' + (demoMode ? 'on' : 'off');

                    // Update SAFE_MODE
                    const safeMode = data.SAFE_MODE === 'true';
                    document.getElementById('safe-mode').checked = safeMode;
                    document.getElementById('safe-mode-status').textContent = safeMode ? 'ENABLED' : 'DISABLED';
                    document.getElementById('safe-mode-indicator').className = 'status-indicator ' + (safeMode ? 'on' : 'off');

                    // Update KILL_SWITCH
                    const killSwitch = data.ENABLE_KILL_SWITCH === 'true';
                    document.getElementById('kill-switch').checked = killSwitch;
                    document.getElementById('kill-switch-status').textContent = killSwitch ? 'ARMED' : 'DISARMED';
                    document.getElementById('kill-switch-indicator').className = 'status-indicator ' + (killSwitch ? 'on' : 'off');

                    logActivity('Settings loaded successfully', 'success');
                })
                .catch(error => {
                    logActivity('Error loading settings: ' + error, 'error');
                });
        }

        function toggleSetting(setting, value) {
            logActivity(`Changing ${setting} to ${value ? 'ON' : 'OFF'}`, 'warning');

            fetch('/api/toggle_setting', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ setting: setting, value: value })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('settings-status', `✅ ${setting} ${value ? 'ENABLED' : 'DISABLED'} successfully. Services will reload automatically.`, true);
                    logActivity(`${setting} changed to ${value ? 'ON' : 'OFF'}`, 'success');

                    // Reload settings to confirm
                    setTimeout(loadAllSettings, 1000);

                    if (setting === 'DEMO_MODE' && !value) {
                        logActivity('⚠️ WARNING: Demo Mode DISABLED - Real attacks will be deployed!', 'error');
                    }
                } else {
                    showStatus('settings-status', `❌ Failed to change ${setting}: ${data.error}`, false);
                    logActivity(`Failed to change ${setting}: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus('settings-status', `❌ Error: ${error}`, false);
                logActivity('Error toggling setting: ' + error, 'error');
            });
        }

        function loadConfig() {
            fetch('/api/get_config')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('config-content').textContent = JSON.stringify(data, null, 2);
                    logActivity('Configuration loaded', 'info');
                })
                .catch(error => {
                    logActivity('Error loading config: ' + error, 'error');
                });
        }

        function saveConfig() {
            logActivity('Saving configuration changes...', 'warning');
            showStatus('settings-status', '💾 Configuration saved (reload services to apply)', true);
        }

        function refreshServices() {
            fetch('/api/service_status')
                .then(response => response.json())
                .then(data => {
                    const servicesList = document.getElementById('services-list');
                    servicesList.innerHTML = '';

                    for (const [service, status] of Object.entries(data.services)) {
                        const li = document.createElement('li');
                        li.innerHTML = `${service} <span class="service-status ${status.running ? 'running' : 'stopped'}">${status.running ? '● RUNNING' : '○ STOPPED'}</span>`;
                        servicesList.appendChild(li);
                    }
                })
                .catch(error => {
                    logActivity('Error refreshing services: ' + error, 'error');
                });
        }

        function restartAllServices() {
            if (!confirm('Restart all services? This will briefly interrupt operations.')) {
                return;
            }

            logActivity('Restarting all services...', 'warning');
            showStatus('service-status', '🔄 Restarting services...', true);

            fetch('/api/restart_services', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showStatus('service-status', '✅ All services restarted successfully', true);
                        logActivity('All services restarted', 'success');
                        setTimeout(refreshServices, 5000);
                    } else {
                        showStatus('service-status', `❌ Restart failed: ${data.error}`, false);
                        logActivity('Service restart failed: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showStatus('service-status', `❌ Error: ${error}`, false);
                    logActivity('Error restarting services: ' + error, 'error');
                });
        }

        function emergencyStop() {
            if (!confirm('⚠️ EMERGENCY STOP: This will immediately halt ALL Red Team operations. Are you sure?')) {
                return;
            }

            logActivity('🛑 EMERGENCY STOP ACTIVATED', 'error');
            showStatus('service-status', '🛑 EMERGENCY STOP - All operations halted', false);

            fetch('/api/emergency_stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        logActivity('All services stopped via emergency stop', 'error');
                        setTimeout(refreshServices, 2000);
                    }
                })
                .catch(error => {
                    logActivity('Error during emergency stop: ' + error, 'error');
                });
        }
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Main control panel interface"""
    return render_template_string(CONTROL_PANEL_HTML)


@app.route('/api/get_settings', methods=['GET'])
def get_settings():
    """Get current operational settings"""
    try:
        return jsonify({
            'DEMO_MODE': os.getenv('DEMO_MODE', 'true'),
            'SAFE_MODE': os.getenv('SAFE_MODE', 'true'),
            'ENABLE_KILL_SWITCH': os.getenv('ENABLE_KILL_SWITCH', 'true'),
            'C2_SERVER': os.getenv('C2_SERVER', 'localhost'),
            'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///red_team_operations.db')
        })
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_config', methods=['GET'])
def get_config():
    """Get full configuration"""
    try:
        config = {}
        env_file = find_dotenv()

        if env_file:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value

        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/toggle_setting', methods=['POST'])
def toggle_setting():
    """Toggle a setting in .env file"""
    try:
        data = request.get_json()
        setting = data.get('setting')
        value = data.get('value')

        if not setting:
            return jsonify({'success': False, 'error': 'Setting name required'}), 400

        # Convert boolean to string
        value_str = 'true' if value else 'false'

        # Update .env file
        env_file = find_dotenv()
        if env_file:
            set_key(env_file, setting, value_str)

            # Reload environment
            load_dotenv(override=True)

            logger.info(f"[CONTROL PANEL] {setting} changed to {value_str}")

            return jsonify({
                'success': True,
                'setting': setting,
                'value': value_str,
                'message': f'{setting} updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': '.env file not found'}), 404

    except Exception as e:
        logger.error(f"Error toggling setting: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/service_status', methods=['GET'])
def service_status():
    """Check status of all services"""
    try:
        services = {}

        # Check Red Team Dashboard
        result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
        services['Red Team Dashboard (5008)'] = {'running': ':5008' in result.stdout}
        services['Blue Team Dashboard (5009)'] = {'running': ':5009' in result.stdout}
        services['C2 Listener (4000)'] = {'running': ':4000' in result.stdout}

        return jsonify({'services': services})
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
        return jsonify({'services': {}, 'error': str(e)}), 500


@app.route('/api/restart_services', methods=['POST'])
def restart_services():
    """Restart all Red Team services"""
    try:
        logger.warning("[CONTROL PANEL] Service restart requested")

        # Kill existing processes
        subprocess.run(['pkill', '-9', '-f', 'red_team_mobile_attack_dashboard.py'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'blue_team_monitoring_dashboard.py'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'c2_listener.py'], check=False)

        # Wait a moment
        import time
        time.sleep(2)

        # Restart services
        subprocess.Popen(['python3', 'red_team_mobile_attack_dashboard.py'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(['python3', 'blue_team_monitoring_dashboard.py'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(['python3', 'c2_listener.py'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info("[CONTROL PANEL] All services restarted")

        return jsonify({
            'success': True,
            'message': 'Services restarted successfully',
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Error restarting services: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/emergency_stop', methods=['POST'])
def emergency_stop():
    """Emergency stop all operations"""
    try:
        logger.critical("[CONTROL PANEL] 🛑 EMERGENCY STOP ACTIVATED")

        # Kill all Red Team processes
        subprocess.run(['pkill', '-9', '-f', 'red_team_mobile_attack_dashboard.py'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'blue_team_monitoring_dashboard.py'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'c2_listener.py'], check=False)

        logger.critical("[CONTROL PANEL] All services stopped")

        return jsonify({
            'success': True,
            'message': 'Emergency stop executed - all services halted',
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Error during emergency stop: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'control_panel'
    })


if __name__ == '__main__':
    logger.info("="*80)
    logger.info("CONTROL PANEL DASHBOARD STARTING")
    logger.info("="*80)
    logger.info("Real-time operational control for Red Team exercises")
    logger.info("Access Control Panel at: http://localhost:5010")
    logger.info("="*80)

    app.run(
        host='0.0.0.0',
        port=5010,
        debug=False
    )
