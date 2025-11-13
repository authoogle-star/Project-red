#!/usr/bin/env python3
"""
Blue Team Monitoring Dashboard
Real-time threat analysis and monitoring for Red Team mobile attack simulations
SOC interface for detecting and analyzing mobile threat vectors
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import func, desc

# Import database models
from database.models import SessionLocal, AttackSimulation, AuditLog

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/blue_team_monitoring.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize database session
db_session = SessionLocal()

# Blue Team Monitoring Dashboard HTML
BLUE_TEAM_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blue Team SOC - Mobile Threat Monitoring</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Courier New', monospace;
            background: #000814;
            color: #00b4d8;
            padding: 20px;
        }
        .header {
            text-align: center;
            border: 3px solid #0077b6;
            padding: 25px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #001d3d 0%, #000814 100%);
            box-shadow: 0 0 20px #0077b6;
        }
        .header h1 {
            color: #00b4d8;
            text-shadow: 0 0 15px #00b4d8, 0 0 30px #00b4d8;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header h2 {
            color: #90e0ef;
            text-shadow: 0 0 10px #90e0ef;
        }
        .container {
            max-width: 1600px;
            margin: 0 auto;
        }
        .section {
            background: linear-gradient(135deg, #001d3d 0%, #000814 100%);
            border: 2px solid #0077b6;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 0 15px rgba(0, 119, 182, 0.3);
        }
        .section h2 {
            color: #00b4d8;
            margin-bottom: 20px;
            border-bottom: 2px solid #0077b6;
            padding-bottom: 10px;
            text-shadow: 0 0 10px #00b4d8;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-box {
            background: #000814;
            padding: 20px;
            border: 2px solid #0077b6;
            text-align: center;
            box-shadow: 0 0 15px rgba(0, 119, 182, 0.3);
        }
        .stat-box.alert {
            border-color: #ff006e;
            box-shadow: 0 0 15px rgba(255, 0, 110, 0.5);
        }
        .stat-value {
            font-size: 2.5em;
            color: #00b4d8;
            font-weight: bold;
            text-shadow: 0 0 10px #00b4d8;
        }
        .stat-value.critical {
            color: #ff006e;
            text-shadow: 0 0 10px #ff006e;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .stat-label {
            color: #90e0ef;
            margin-top: 10px;
            font-size: 1.1em;
        }
        .threat-feed {
            background: #000814;
            border: 2px solid #0077b6;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        .threat-item {
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #0077b6;
            background: #001d3d;
        }
        .threat-item.critical {
            border-left-color: #ff006e;
            background: #1a0010;
        }
        .threat-item.high {
            border-left-color: #fb8500;
            background: #1a0f00;
        }
        .threat-item.medium {
            border-left-color: #ffb703;
            background: #1a1400;
        }
        .threat-item.low {
            border-left-color: #06d6a0;
            background: #001a14;
        }
        .threat-title {
            color: #00b4d8;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .threat-details {
            color: #90e0ef;
            font-size: 12px;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            margin-right: 5px;
            font-size: 10px;
            font-weight: bold;
            border-radius: 3px;
        }
        .badge.critical { background: #ff006e; color: #fff; }
        .badge.high { background: #fb8500; color: #000; }
        .badge.medium { background: #ffb703; color: #000; }
        .badge.low { background: #06d6a0; color: #000; }
        .badge.ios { background: #0077b6; color: #fff; }
        .badge.android { background: #06d6a0; color: #000; }
        .alert-banner {
            background: linear-gradient(135deg, #1a0010 0%, #330020 100%);
            border: 3px solid #ff006e;
            padding: 20px;
            margin-bottom: 25px;
            color: #ff006e;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 0, 110, 0.5);
            animation: pulse-banner 3s infinite;
        }
        @keyframes pulse-banner {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 110, 0.5); }
            50% { box-shadow: 0 0 30px rgba(255, 0, 110, 0.8); }
        }
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        .timeline-item {
            padding: 15px;
            margin-bottom: 15px;
            border-left: 3px solid #0077b6;
            margin-left: 20px;
            position: relative;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -8px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #0077b6;
            box-shadow: 0 0 10px #0077b6;
        }
        .filter-controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-btn {
            background: #0077b6;
            color: #fff;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            transition: all 0.3s;
        }
        .filter-btn:hover {
            background: #00b4d8;
            box-shadow: 0 0 15px rgba(0, 180, 216, 0.5);
        }
        .filter-btn.active {
            background: #ff006e;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #0077b6;
        }
        th {
            background: #001d3d;
            color: #00b4d8;
            font-weight: bold;
        }
        tr:hover {
            background: #001d3d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ BLUE TEAM SOC - MOBILE THREAT MONITORING 🛡️</h1>
            <h2>Real-Time Analysis & Detection System</h2>
            <p style="color: #90e0ef; margin-top: 10px;">Monitoring Red Team Mobile Attack Simulations</p>
        </div>

        <div id="alert-container"></div>

        <!-- Threat Statistics -->
        <div class="section">
            <h2>📊 Threat Intelligence Dashboard</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value" id="stat-total-threats">-</div>
                    <div class="stat-label">Total Threats Detected</div>
                </div>
                <div class="stat-box alert">
                    <div class="stat-value critical" id="stat-active-attacks">-</div>
                    <div class="stat-label">Active Attacks</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-ios-threats">-</div>
                    <div class="stat-label">iOS Threats</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-android-threats">-</div>
                    <div class="stat-label">Android Threats</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-blocked">-</div>
                    <div class="stat-label">Blocked/Mitigated</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-detection-rate">-</div>
                    <div class="stat-label">Detection Rate</div>
                </div>
            </div>
        </div>

        <!-- Real-Time Threat Feed -->
        <div class="section">
            <h2>🚨 Real-Time Threat Feed</h2>
            <div class="filter-controls">
                <button class="filter-btn active" onclick="filterThreats('all')">All Threats</button>
                <button class="filter-btn" onclick="filterThreats('critical')">Critical</button>
                <button class="filter-btn" onclick="filterThreats('ios')">iOS</button>
                <button class="filter-btn" onclick="filterThreats('android')">Android</button>
                <button class="filter-btn" onclick="filterThreats('whatsapp')">WhatsApp</button>
            </div>
            <div class="threat-feed" id="threat-feed">
                <div style="color: #00b4d8; text-align: center; padding: 20px;">
                    [System] Initializing threat detection systems...<br>
                    [System] Monitoring Red Team mobile attack vectors...<br>
                    [System] Real-time analysis active...
                </div>
            </div>
        </div>

        <!-- Recent Attack Timeline -->
        <div class="section">
            <h2>⏱️ Attack Timeline (Last 24 Hours)</h2>
            <div class="timeline" id="attack-timeline">
                <!-- Timeline items will be populated here -->
            </div>
        </div>

        <!-- Detailed Threat Analysis -->
        <div class="section">
            <h2>🔍 Detailed Threat Analysis</h2>
            <table id="threat-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Threat Type</th>
                        <th>Target</th>
                        <th>Platform</th>
                        <th>Delivery Method</th>
                        <th>Status</th>
                        <th>CVE</th>
                    </tr>
                </thead>
                <tbody id="threat-table-body">
                    <tr>
                        <td colspan="7" style="text-align: center; color: #90e0ef;">Loading threat data...</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        let currentFilter = 'all';

        // Load data on page load
        window.addEventListener('load', function() {
            loadAllData();
            setInterval(loadAllData, 5000);  // Refresh every 5 seconds for real-time monitoring
        });

        function loadAllData() {
            loadStatistics();
            loadThreatFeed();
            loadAttackTimeline();
            loadThreatTable();
        }

        function loadStatistics() {
            fetch('/api/blue_team_stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('stat-total-threats').textContent = data.total_threats || 0;
                    document.getElementById('stat-active-attacks').textContent = data.active_attacks || 0;
                    document.getElementById('stat-ios-threats').textContent = data.ios_threats || 0;
                    document.getElementById('stat-android-threats').textContent = data.android_threats || 0;
                    document.getElementById('stat-blocked').textContent = data.blocked_threats || 0;
                    document.getElementById('stat-detection-rate').textContent = (data.detection_rate || 0).toFixed(1) + '%';

                    // Show alert banner if active attacks detected
                    if (data.active_attacks > 0) {
                        showAlertBanner(data.active_attacks);
                    } else {
                        hideAlertBanner();
                    }
                })
                .catch(error => console.error('Error loading stats:', error));
        }

        function loadThreatFeed() {
            fetch('/api/threat_feed')
                .then(response => response.json())
                .then(data => {
                    const feed = document.getElementById('threat-feed');
                    feed.innerHTML = '';

                    if (data.threats && data.threats.length > 0) {
                        data.threats.forEach(threat => {
                            if (currentFilter === 'all' ||
                                threat.severity === currentFilter ||
                                threat.platform === currentFilter ||
                                threat.delivery_method === currentFilter) {

                                const item = document.createElement('div');
                                item.className = `threat-item ${threat.severity}`;
                                item.innerHTML = `
                                    <div class="threat-title">
                                        <span class="badge ${threat.severity}">${threat.severity.toUpperCase()}</span>
                                        <span class="badge ${threat.platform}">${threat.platform.toUpperCase()}</span>
                                        ${threat.title}
                                    </div>
                                    <div class="threat-details">
                                        <strong>Target:</strong> ${threat.target} |
                                        <strong>Delivery:</strong> ${threat.delivery_method} |
                                        <strong>Time:</strong> ${threat.timestamp}<br>
                                        <strong>Attack Type:</strong> ${threat.attack_type} |
                                        <strong>CVE:</strong> ${threat.cve || 'N/A'}
                                    </div>
                                `;
                                feed.appendChild(item);
                            }
                        });
                    } else {
                        feed.innerHTML = '<div style="color: #90e0ef; text-align: center; padding: 20px;">No threats detected</div>';
                    }
                })
                .catch(error => console.error('Error loading threat feed:', error));
        }

        function loadAttackTimeline() {
            fetch('/api/attack_timeline')
                .then(response => response.json())
                .then(data => {
                    const timeline = document.getElementById('attack-timeline');
                    timeline.innerHTML = '';

                    if (data.timeline && data.timeline.length > 0) {
                        data.timeline.forEach(item => {
                            const timelineItem = document.createElement('div');
                            timelineItem.className = 'timeline-item';
                            timelineItem.innerHTML = `
                                <div style="color: #00b4d8; font-weight: bold;">${item.timestamp}</div>
                                <div style="color: #90e0ef;">${item.description}</div>
                            `;
                            timeline.appendChild(timelineItem);
                        });
                    } else {
                        timeline.innerHTML = '<div style="color: #90e0ef; padding: 20px;">No recent attacks</div>';
                    }
                })
                .catch(error => console.error('Error loading timeline:', error));
        }

        function loadThreatTable() {
            fetch('/api/threat_details')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('threat-table-body');
                    tbody.innerHTML = '';

                    if (data.threats && data.threats.length > 0) {
                        data.threats.forEach(threat => {
                            const row = tbody.insertRow();
                            row.innerHTML = `
                                <td>${threat.timestamp}</td>
                                <td>${threat.attack_type}</td>
                                <td>${threat.target}</td>
                                <td><span class="badge ${threat.platform}">${threat.platform}</span></td>
                                <td>${threat.delivery_method}</td>
                                <td>${threat.status}</td>
                                <td>${threat.cve || 'N/A'}</td>
                            `;
                        });
                    } else {
                        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #90e0ef;">No threat data available</td></tr>';
                    }
                })
                .catch(error => console.error('Error loading threat details:', error));
        }

        function filterThreats(filter) {
            currentFilter = filter;

            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Reload threat feed with filter
            loadThreatFeed();
        }

        function showAlertBanner(activeCount) {
            let banner = document.getElementById('alert-banner');
            if (!banner) {
                banner = document.createElement('div');
                banner.id = 'alert-banner';
                banner.className = 'alert-banner';
                document.querySelector('.container').insertBefore(banner, document.querySelector('.container').children[1]);
            }
            banner.innerHTML = `
                <strong>🚨 ACTIVE MOBILE ATTACKS DETECTED 🚨</strong><br>
                ${activeCount} active attack simulation(s) in progress<br>
                <strong>SOC Alert Level: HIGH</strong>
            `;
        }

        function hideAlertBanner() {
            const banner = document.getElementById('alert-banner');
            if (banner) {
                banner.remove();
            }
        }
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Main Blue Team monitoring dashboard"""
    return render_template_string(BLUE_TEAM_DASHBOARD_HTML)


@app.route('/api/blue_team_stats', methods=['GET'])
def get_blue_team_statistics():
    """Get Blue Team statistics"""
    try:
        # Count total mobile threats
        total_threats = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%mobile%')
        ).scalar() or 0

        # Count active attacks (last 5 minutes)
        five_min_ago = datetime.utcnow() - timedelta(minutes=5)
        active_attacks = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%mobile%'),
            AttackSimulation.timestamp >= five_min_ago
        ).scalar() or 0

        # iOS threats
        ios_threats = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%ios%')
        ).scalar() or 0

        # Android threats
        android_threats = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%android%')
        ).scalar() or 0

        # Blocked threats
        blocked_threats = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%mobile%'),
            AttackSimulation.status == 'BLOCKED_UNAUTHORIZED'
        ).scalar() or 0

        # Detection rate
        detected = db_session.query(func.count(AttackSimulation.id)).filter(
            AttackSimulation.attack_type.like('%mobile%'),
            AttackSimulation.status.in_(['SUCCESS', 'BLOCKED_UNAUTHORIZED', 'DEMO_SUCCESS'])
        ).scalar() or 0

        detection_rate = (detected / total_threats * 100) if total_threats > 0 else 100

        return jsonify({
            'total_threats': total_threats,
            'active_attacks': active_attacks,
            'ios_threats': ios_threats,
            'android_threats': android_threats,
            'blocked_threats': blocked_threats,
            'detection_rate': detection_rate
        })

    except Exception as e:
        logger.error(f"Error getting Blue Team statistics: {e}")
        return jsonify({
            'total_threats': 0,
            'active_attacks': 0,
            'ios_threats': 0,
            'android_threats': 0,
            'blocked_threats': 0,
            'detection_rate': 0
        })


@app.route('/api/threat_feed', methods=['GET'])
def get_threat_feed():
    """Get real-time threat feed"""
    try:
        # Get last 20 mobile attacks
        attacks = db_session.query(AttackSimulation).filter(
            AttackSimulation.attack_type.like('%mobile%')
        ).order_by(desc(AttackSimulation.timestamp)).limit(20).all()

        threats = []
        for attack in attacks:
            details = json.loads(attack.details) if attack.details else {}

            # Determine severity
            severity = 'medium'
            if 'zero_click' in attack.attack_type or 'webkit' in attack.attack_type:
                severity = 'critical'
            elif 'bluetooth' in attack.attack_type:
                severity = 'high'
            elif attack.status == 'BLOCKED_UNAUTHORIZED':
                severity = 'low'

            threats.append({
                'title': f"Mobile Attack Detected: {attack.attack_type}",
                'severity': severity,
                'platform': details.get('platform', 'unknown'),
                'target': attack.target,
                'delivery_method': details.get('delivery_method', 'unknown'),
                'attack_type': attack.attack_type,
                'cve': details.get('cve', 'N/A'),
                'timestamp': attack.timestamp.strftime('%Y-%m-%d %H:%M:%S') if attack.timestamp else 'N/A'
            })

        return jsonify({'threats': threats})

    except Exception as e:
        logger.error(f"Error getting threat feed: {e}")
        return jsonify({'threats': []})


@app.route('/api/attack_timeline', methods=['GET'])
def get_attack_timeline():
    """Get attack timeline for last 24 hours"""
    try:
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

        attacks = db_session.query(AttackSimulation).filter(
            AttackSimulation.attack_type.like('%mobile%'),
            AttackSimulation.timestamp >= twenty_four_hours_ago
        ).order_by(desc(AttackSimulation.timestamp)).all()

        timeline = []
        for attack in attacks:
            details = json.loads(attack.details) if attack.details else {}
            timeline.append({
                'timestamp': attack.timestamp.strftime('%H:%M:%S') if attack.timestamp else 'N/A',
                'description': f"{attack.attack_type} on {attack.target} via {details.get('delivery_method', 'unknown')} - {attack.status}"
            })

        return jsonify({'timeline': timeline})

    except Exception as e:
        logger.error(f"Error getting attack timeline: {e}")
        return jsonify({'timeline': []})


@app.route('/api/threat_details', methods=['GET'])
def get_threat_details():
    """Get detailed threat information"""
    try:
        attacks = db_session.query(AttackSimulation).filter(
            AttackSimulation.attack_type.like('%mobile%')
        ).order_by(desc(AttackSimulation.timestamp)).limit(50).all()

        threats = []
        for attack in attacks:
            details = json.loads(attack.details) if attack.details else {}
            threats.append({
                'timestamp': attack.timestamp.strftime('%Y-%m-%d %H:%M:%S') if attack.timestamp else 'N/A',
                'attack_type': attack.attack_type,
                'target': attack.target,
                'platform': details.get('platform', 'unknown'),
                'delivery_method': details.get('delivery_method', 'unknown'),
                'status': attack.status,
                'cve': details.get('cve', 'N/A')
            })

        return jsonify({'threats': threats})

    except Exception as e:
        logger.error(f"Error getting threat details: {e}")
        return jsonify({'threats': []})


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'blue_team_monitoring'
    })


if __name__ == '__main__':
    logger.info("="*80)
    logger.info("BLUE TEAM MONITORING DASHBOARD STARTING")
    logger.info("="*80)
    logger.info("Real-time threat analysis and detection active")
    logger.info("Access Blue Team dashboard at: http://localhost:5009")
    logger.info("="*80)

    app.run(
        host='0.0.0.0',
        port=5009,
        debug=False
    )
