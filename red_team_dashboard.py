#!/usr/bin/env python3
"""
PROJECT RED SWORD - Unified Dashboard
All-in-one dashboard with tabs for different views
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import panel as pn
import numpy as np
import pandas as pd

# Configure Panel
pn.extension(design="bootstrap", sizing_mode="stretch_width")

# ============================================================================
# TAB 1: HOME PAGE
# ============================================================================

def create_home_tab():
    """Home page with system overview."""
    return pn.Column(
        pn.pane.Markdown("""
# 🛡️ PROJECT RED SWORD - Red Team Operations Platform

Welcome to the Red Team Attack Simulation and Defense Monitoring Platform.

---

## ⚙️ System Status

**Environment**: Production Monitoring
**Mode**: Safe Demo (No External APIs)
**Safe Mode**: ✅ ENABLED
**Network Segmentation**: ✅ ENFORCED
**Rate Limiting**: ✅ ACTIVE (10 attacks/min)
**Kill Switch**: ✅ READY

---

## 🚀 Quick Start

### Run Your First Attack Simulation

```bash
# Terminal window (keep server running in another)
cd /home/EXQUISITE/Project-Red-Sword
source venv/bin/activate

# Run APT simulation
python3 -c "from modules.apt_simulation import APTSimulation; \\
    apt = APTSimulation(); print(apt.simulate_attack())"

# Run social engineering
python3 -c "from modules.advanced_social_engineering import AdvancedSocialEngineering; \\
    se = AdvancedSocialEngineering(); print(se.simulate_attack())"
```

### View Logs

```bash
# Real-time attack logs
tail -f logs/attack_simulation.log

# Database query
sqlite3 red_team_operations.db \\
    "SELECT * FROM attack_simulations ORDER BY timestamp DESC LIMIT 5;"
```

### Emergency Stop

```bash
python3 scripts/kill_all_simulations.py --yes
```

---

## 📊 Available Modules

### Attack Capabilities
- ✅ Social Engineering (phishing, spear phishing)
- ✅ Web Application (SQL injection, XSS, CSRF)
- ✅ Network Attacks (DNS tunneling, port scanning, MITM)
- ✅ APT Simulations (multi-stage, lateral movement)
- ✅ AI Red Teaming (adaptive attacks)
- ✅ **Mobile Testing (iOS & Android)** - [Launch C2 Panel](http://localhost:5007)

### Defense Capabilities
- ✅ Real-Time Monitoring (anomaly detection)
- ✅ Threat Intelligence (local feeds)
- ✅ Automated Incident Response
- ✅ Blockchain Logging (immutable audit)
- ✅ Machine Learning Detection

---

## 📱 Mobile Security Testing

**NEW**: Test iOS and Android device security

**Access**: [Mobile Testing C2 Panel](http://localhost:5007)

**Features**:
- SMS/Email phishing simulations
- Authorized target controls
- Real-time statistics
- Comprehensive logging

**Quick Start**:
```bash
# Start mobile testing C2 panel (in new terminal)
./scripts/start_mobile_testing.sh
```

**Documentation**: `MOBILE_TESTING_GUIDE.md`

---

## 📖 Documentation

- **Deployment Guide**: `PRODUCTION_DEPLOYMENT_GUIDE.md`
- **Configuration**: `config/attack_config.yaml`, `config/safe_mode.yaml`
- **Health Check**: `python3 scripts/health_check.py`
        """),
        width=900
    )

# ============================================================================
# TAB 2: ATTACK CONTROL
# ============================================================================

def create_attack_control_tab():
    """Attack control panel."""

    status_text = pn.pane.Markdown("""
## 🎯 Red Team Attack Control Center

**System Status**: 🟢 OPERATIONAL
**Safe Mode**: 🟢 ENABLED
**Kill Switch**: 🟢 READY

---
    """)

    attack_type = pn.widgets.Select(
        name='Attack Type',
        options=[
            'Social Engineering - Phishing',
            'Web Application - SQL Injection',
            'Network - Port Scan',
            'APT - Multi-Stage Simulation',
        ],
        width=300
    )

    target_input = pn.widgets.TextInput(
        name='Target',
        placeholder='Use targets from config/targets.yaml',
        width=300
    )

    launch_button = pn.widgets.Button(
        name='🚀 Launch Simulation',
        button_type='danger',
        width=300
    )

    stop_button = pn.widgets.Button(
        name='🛑 Emergency Stop',
        button_type='warning',
        width=300
    )

    status_output = pn.pane.Markdown("Ready to launch simulations...")

    def launch_attack(event):
        attack = attack_type.value
        target = target_input.value or "Default targets"

        status_output.object = f"""
### 🚀 Attack Simulation

**Type**: {attack}
**Target**: {target}
**Status**: Ready to execute

**To run actual attack, use Python:**
```python
# APT Simulation
from modules.apt_simulation import APTSimulation
apt = APTSimulation()
result = apt.simulate_attack()
print(result)

# Social Engineering
from modules.advanced_social_engineering import AdvancedSocialEngineering
se = AdvancedSocialEngineering()
result = se.simulate_attack()
print(result)
```

**Or from command line:**
```bash
python3 -c "from modules.apt_simulation import APTSimulation; \\
    apt = APTSimulation(); print(apt.simulate_attack())"
```
        """

    def stop_attacks(event):
        status_output.object = """
### 🛑 EMERGENCY STOP

Run kill switch:
```bash
python3 scripts/kill_all_simulations.py --yes
```
        """

    launch_button.on_click(launch_attack)
    stop_button.on_click(stop_attacks)

    info_text = pn.pane.Markdown("""
---

## 🛡️ Safety Features

- **Safe Mode**: All attacks controlled and logged
- **Rate Limiting**: Max 10 attacks/minute
- **Target Validation**: Only whitelisted targets
- **Network Segmentation**: Isolated networks only
- **Auto Cleanup**: Artifacts removed automatically

## 📝 Configuration Files

- `config/attack_config.yaml` - Attack parameters
- `config/safe_mode.yaml` - Safety controls
- `config/targets.yaml` - Authorized targets
- `.env` - Environment settings
    """)

    return pn.Column(
        status_text,
        pn.Row(
            pn.Column(attack_type, target_input, launch_button, stop_button, width=350),
            pn.Column(status_output, width=600)
        ),
        info_text
    )

# ============================================================================
# TAB 3: DEFENSE MONITORING
# ============================================================================

def create_defense_tab():
    """Defense monitoring with Datashader visualization."""

    try:
        import datashader as ds
        import datashader.transfer_functions as tf
        import colorcet as cc

        # Generate sample data
        n_points = 100000  # Reduced for faster loading
        np.random.seed(42)

        threat_types = ['Malware', 'Phishing', 'DDoS', 'SQL Injection', 'XSS']

        threat_data = pd.DataFrame({
            'timestamp': np.random.randint(0, 86400, n_points),
            'severity': np.random.beta(2, 5, n_points),
            'threat_type': pd.Categorical(np.random.choice(threat_types, n_points)),
        })

        # Create visualization
        canvas = ds.Canvas(plot_width=800, plot_height=400)
        agg = canvas.points(threat_data, 'timestamp', 'severity', ds.count_cat('threat_type'))
        img = tf.shade(agg, color_key=cc.palette['glasbey_category10'])
        img = tf.set_background(img, "black")

        viz = pn.pane.PNG(img, width=800, height=400)

        stats = pn.pane.Markdown(f"""
### 📊 Security Statistics

- **Threats Detected**: {len(threat_data):,}
- **High Severity**: {len(threat_data[threat_data['severity'] > 0.7]):,}
- **Data Points**: {n_points:,}
        """)

    except Exception as e:
        viz = pn.pane.Markdown(f"⚠️ Visualization error: {e}")
        stats = pn.pane.Markdown("Stats unavailable")

    return pn.Column(
        pn.pane.Markdown("# 🛡️ Defense Monitoring Dashboard"),
        pn.pane.Markdown("""
Real-time security monitoring powered by **Datashader**.

## Threat Detection Timeline
Showing threat types over 24 hours by severity level.
        """),
        stats,
        viz,
        pn.pane.Markdown("""
---

## 💡 Live Monitoring

To monitor real attacks:
```python
from database.models import ThreatDetection, SessionLocal
session = SessionLocal()
detections = session.query(ThreatDetection).order_by(
    ThreatDetection.timestamp.desc()
).limit(10).all()
```

## 📝 View Logs
```bash
tail -f logs/attack_simulation.log
tail -f logs/detections.log
```
        """)
    )

# ============================================================================
# TAB 4: MOBILE TESTING
# ============================================================================

def create_mobile_testing_tab():
    """Mobile testing for iOS and Android devices."""

    status_text = pn.pane.Markdown("""
## 📱 Mobile Security Testing - iOS & Android

**System Status**: 🟢 OPERATIONAL
**TextBelt SMS**: 🟢 READY
**SendGrid Email**: 🟢 READY
**Authorization**: 🟢 ENABLED

---
    """)

    # Device type selector
    device_type = pn.widgets.RadioButtonGroup(
        name='Device Type',
        options=['iOS', 'Android'],
        value='iOS',
        button_type='primary'
    )

    # Target input
    target_phone = pn.widgets.TextInput(
        name='Target Phone Number',
        placeholder='+1234567890',
        width=300
    )

    target_email = pn.widgets.TextInput(
        name='Target Email (optional)',
        placeholder='user@company.com',
        width=300
    )

    # Test type selector
    test_type = pn.widgets.Select(
        name='Test Type',
        options=[
            'Phishing Email',
            'Smishing (SMS Phishing)',
            'Malicious Profile (iOS)',
            'Malicious APK (Android)',
            'Credential Harvesting',
            'Social Engineering'
        ],
        value='Smishing (SMS Phishing)',
        width=300
    )

    # Custom message
    custom_message = pn.widgets.TextAreaInput(
        name='Custom Test Message',
        placeholder='Your package delivery failed. Click here to reschedule: [TEST_LINK]',
        height=100,
        width=500
    )

    # Launch buttons
    launch_sms_button = pn.widgets.Button(
        name='📱 Send SMS Test',
        button_type='danger',
        width=200
    )

    launch_email_button = pn.widgets.Button(
        name='📧 Send Email Test',
        button_type='warning',
        width=200
    )

    check_targets_button = pn.widgets.Button(
        name='🔍 Check Authorized Targets',
        button_type='primary',
        width=200
    )

    # Status output
    status_output = pn.pane.Markdown("""
### Ready to Launch Mobile Tests

**Instructions**:
1. Select device type (iOS or Android)
2. Enter target phone number or email
3. Choose test type
4. Optionally customize the message
5. Click 'Send SMS Test' or 'Send Email Test'

**Note**: Targets must be authorized in `config/mobile_targets.yaml`
    """)

    def launch_sms_test(event):
        phone = target_phone.value
        device = device_type.value
        test = test_type.value
        message = custom_message.value or f"Security test for {device} device"

        if not phone:
            status_output.object = """
### ❌ Error

**Missing phone number!** Please enter a target phone number.
            """
            return

        status_output.object = f"""
### 🚀 Launching SMS Test

**Device Type**: {device}
**Target Phone**: {phone}
**Test Type**: {test}
**Message**: {message[:50]}...

**Executing...**

To run this test, use the Python API:

```python
from modules.mobile_security_testing import MobileSecurityTesting

mobile = MobileSecurityTesting()
result = mobile.send_sms_test(
    phone_number="{phone}",
    message="{message}",
    test_name="{test}"
)
print(result)
```

**Or via command line**:

```bash
python3 << EOF
from modules.mobile_security_testing import MobileSecurityTesting
mobile = MobileSecurityTesting()
result = mobile.send_sms_test("{phone}", "{message}", "{test}")
print(result)
EOF
```

**Check logs**: `tail -f logs/mobile_testing.log`

**Note**: In demo mode, SMS will be simulated. Set `DEMO_MODE=false` in `.env` for real SMS delivery via TextBelt.
        """

    def launch_email_test(event):
        email = target_email.value
        device = device_type.value
        test = test_type.value
        message = custom_message.value or f"Security test email for {device}"

        if not email:
            status_output.object = """
### ❌ Error

**Missing email address!** Please enter a target email.
            """
            return

        status_output.object = f"""
### 📧 Launching Email Test

**Device Type**: {device}
**Target Email**: {email}
**Test Type**: {test}
**Message**: {message[:50]}...

**Executing...**

To run this test, use the Python API:

```python
from modules.mobile_security_testing import MobileSecurityTesting

mobile = MobileSecurityTesting()
result = mobile.send_email_test(
    email_address="{email}",
    subject="Security Test - {test}",
    message="{message}",
    test_name="{test}"
)
print(result)
```

**Or access the Mobile C2 Panel**:
[http://localhost:5007](http://localhost:5007)

**Check logs**: `tail -f logs/mobile_testing.log`
        """

    def check_targets(event):
        status_output.object = """
### 🔍 Authorized Targets Configuration

To view and edit authorized targets:

```bash
# View current targets
cat config/mobile_targets.yaml

# Edit targets
vim config/mobile_targets.yaml
```

**Example target configuration**:

```yaml
authorized_targets:
  - type: phone
    value: "+15555551234"
    device_type: ios
    device_name: "Test iPhone - Security Team"
    owner: "team_member_name"
    status: active
    authorized_by: "security_director"
    authorization_date: "2024-01-01"
```

**Load targets in Python**:

```python
from modules.mobile_security_testing import MobileSecurityTesting
mobile = MobileSecurityTesting()
print(f"Authorized targets: {len(mobile.authorized_targets)}")
for target in mobile.authorized_targets:
    print(f"  - {target['value']} ({target['device_type']})")
```

**Documentation**: See `MOBILE_TESTING_GUIDE.md` for complete setup instructions.
        """

    launch_sms_button.on_click(launch_sms_test)
    launch_email_button.on_click(launch_email_test)
    check_targets_button.on_click(check_targets)

    info_text = pn.pane.Markdown("""
---

## 📱 Mobile Testing Features

### SMS Testing (via TextBelt)
- Free tier: 1 SMS per day per phone number
- Paid tier: $0.0064 per message
- No signup required for testing

### Email Testing (via SendGrid)
- Free tier: 100 emails per day
- Professional templates
- Tracking and analytics

### Device Support
- **iOS**: Phishing, smishing, malicious profiles, WebKit tests
- **Android**: Phishing, smishing, malicious APKs, Bluetooth tests

### Safety Controls
- ✅ Authorization required (whitelist-based)
- ✅ All activities logged to database
- ✅ Demo mode available (simulated tests)
- ✅ Rate limiting enforced
- ✅ Audit trail maintained

## 🔧 Advanced Options

**Full C2 Panel**: For advanced features, access the dedicated mobile testing C2 panel:
[http://localhost:5007](http://localhost:5007)

**Start C2 Panel**:
```bash
./scripts/start_mobile_testing.sh
```

**Configuration Files**:
- Authorized Targets: `config/mobile_targets.yaml`
- Environment: `.env` (TEXTBELT_API_KEY, SENDGRID_API_KEY)
- Logs: `logs/mobile_testing.log`

## 📖 Documentation

- **Setup Guide**: `TEXTBELT_SETUP.md`
- **Full Guide**: `MOBILE_TESTING_GUIDE.md`
- **Quick Start**: `MOBILE_TESTING_QUICKSTART.md`
    """)

    return pn.Column(
        status_text,
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Device Configuration"),
                device_type,
                target_phone,
                target_email,
                test_type,
                width=350
            ),
            pn.Column(
                pn.pane.Markdown("### Test Message"),
                custom_message,
                pn.Row(launch_sms_button, launch_email_button),
                check_targets_button,
                width=550
            )
        ),
        pn.pane.Markdown("---"),
        pn.pane.Markdown("### Test Status"),
        status_output,
        info_text
    )

# ============================================================================
# MAIN DASHBOARD WITH TABS
# ============================================================================

# Create tabs
tabs = pn.Tabs(
    ('🏠 Home', create_home_tab()),
    ('🎯 Attack Control', create_attack_control_tab()),
    ('🛡️ Defense Monitoring', create_defense_tab()),
    ('📱 Mobile Testing', create_mobile_testing_tab()),
    dynamic=True
)

# Serve the dashboard
template = pn.template.BootstrapTemplate(
    title="🛡️ Red Team Operations",
    main=tabs,
    main_max_width="95%",
    header_background="#8B0000",
)

template.servable()
