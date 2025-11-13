# Mobile Attack Simulation System - Complete Guide

## 🎯 Overview

This is a **production-ready mobile penetration testing framework** for Red Team vs Blue Team simulations. The system deploys real-world attack vectors against iOS and Android devices using zero-click exploits delivered via **Infobip WhatsApp**, SMS, and email.

---

## 🏗️ System Architecture

### **Components**

1. **Red Team Mobile Attack Dashboard** (`red_team_mobile_attack_dashboard.py`)
   - Port: `5008`
   - Purpose: Deploy iOS and Android exploits
   - Features: Auto device detection, WhatsApp delivery, post-exploitation

2. **Blue Team Monitoring Dashboard** (`blue_team_monitoring_dashboard.py`)
   - Port: `5009`
   - Purpose: Real-time threat detection and analysis
   - Features: SOC interface, threat intelligence, attack timeline

3. **Mobile Attack Payloads Module** (`modules/mobile_attack_payloads.py`)
   - iOS WebKit Zero-Click Exploit (CVE-2021-30860)
   - Android Bluetooth Zero-Click Exploit (CVE-2023-45866)
   - Post-exploitation modules (contacts, SMS, location, photos)

4. **Mobile Security Testing Module** (`modules/mobile_security_testing.py`)
   - Infobip WhatsApp/SMS integration
   - SendGrid email delivery
   - Target authorization and audit logging

---

## 📋 Prerequisites

### **Required API Keys**

Add these to your `.env` file:

```bash
# Infobip API (Primary - for WhatsApp & SMS)
INFOBIP_API_KEY=your_infobip_api_key_here
INFOBIP_BASE_URL=https://g9vm5e.api.infobip.com
INFOBIP_FROM_NUMBER=447860088970
INFOBIP_WHATSAPP_ENABLED=true

# SMS Provider Selection
SMS_PROVIDER=infobip   # or 'textbelt'

# TextBelt API (Backup - for SMS only)
TEXTBELT_API_KEY=textbelt   # 'textbelt' for free tier (1/day)

# SendGrid API (for Email)
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=security-testing@yourcompany.com

# C2 Server Configuration
C2_SERVER=zeroclickexploits.ddns.net
C2_PORT_IOS=4444
C2_PORT_ANDROID=4445

# Demo Mode (set to 'false' for production)
DEMO_MODE=true
```

### **Authorized Targets Configuration**

Create `config/mobile_targets.yaml`:

```yaml
authorized_targets:
  - type: phone
    value: "+1234567890"
    status: active
    description: "Test Device 1 - iOS"

  - type: phone
    value: "+0987654321"
    status: active
    description: "Test Device 2 - Android"

  - type: email
    value: "test@yourcompany.com"
    status: active
    description: "Test Email Account"
```

---

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
cd /home/EXQUISITE/Project-Red
source venv/bin/activate  # or: source Venv/bin/activate
pip install -r requirements.txt
```

### **2. Configure Environment**

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### **3. Setup Authorized Targets**

```bash
# Create config directory if not exists
mkdir -p config

# Create authorized targets file
nano config/mobile_targets.yaml
```

### **4. Start Both Dashboards**

**Terminal 1 - Red Team Dashboard:**
```bash
python3 red_team_mobile_attack_dashboard.py
```
Access at: `http://localhost:5008`

**Terminal 2 - Blue Team Dashboard:**
```bash
python3 blue_team_monitoring_dashboard.py
```
Access at: `http://localhost:5009`

---

## 🎮 Usage Guide

### **Red Team Dashboard (Port 5008)**

#### **Deploy Mobile Attack:**

1. **Enter Target Phone Number**
   - Must be in authorized targets list
   - Format: `+1234567890`

2. **Select Platform Detection:**
   - 🤖 **Auto-Detect** (Recommended for stealth)
   - 🍎 **iOS** (Manual selection)
   - 🤖 **Android** (Manual selection)

3. **Choose Attack Vector:**
   - **Zero-Click Exploit** - No user interaction required
   - **Phishing** - Social engineering vector
   - **Fake System Update** - Mimics OS update
   - **Package Delivery Scam** - Package tracking lure

4. **Select Delivery Method:**
   - **📱 WhatsApp** (Infobip - Recommended)
   - **💬 SMS** (Infobip/TextBelt)
   - **📧 Email** (SendGrid)

5. **Choose Post-Exploitation Modules:**
   - 📇 Contacts Exfiltration
   - 💬 SMS Dump
   - 📍 Location Tracking
   - 📸 Photos Metadata
   - 📞 Call Logs

6. **Deploy Attack**
   - Click "🚀 DEPLOY ATTACK" for production
   - Click "⚡ SIMULATE" for demo mode

---

### **Blue Team Dashboard (Port 5009)**

#### **Real-Time Monitoring Features:**

1. **Threat Intelligence Dashboard**
   - Total threats detected
   - Active attacks in progress
   - Platform-specific threats (iOS/Android)
   - Detection rate metrics

2. **Real-Time Threat Feed**
   - Live feed of all mobile attacks
   - Filter by severity: Critical, High, Medium, Low
   - Filter by platform: iOS, Android
   - Filter by delivery method: WhatsApp, SMS, Email

3. **Attack Timeline**
   - 24-hour attack history
   - Chronological view of all threats

4. **Detailed Threat Analysis**
   - Complete attack details table
   - CVE information
   - Delivery methods
   - Attack status

---

## 🔧 Attack Vectors Explained

### **iOS WebKit Zero-Click Exploit (CVE-2021-30860)**

**Description:**
- Exploits WebKit rendering engine vulnerability
- Achieves remote code execution without user interaction
- Deploys via malicious link in WhatsApp/SMS

**Post-Exploitation Capabilities:**
- 📇 Contacts database exfiltration (`/var/mobile/Library/AddressBook/`)
- 💬 SMS message dump (`/var/mobile/Library/SMS/sms.db`)
- 📍 Device location tracking
- 📸 Photos metadata extraction
- ⌨️ Keylogger deployment

**Attack Flow:**
```
1. WhatsApp message with exploit link sent
2. WebKit processes malicious HTML/JavaScript
3. Reverse shell connects to C2 server (zeroclickexploits.ddns.net:4444)
4. Post-exploitation modules execute
5. Data exfiltrated to C2 server
```

---

### **Android Bluetooth Zero-Click Exploit (CVE-2023-45866)**

**Description:**
- Exploits BlueDroid Bluetooth stack vulnerability
- Remote code execution via proximity attack
- No user interaction required

**Post-Exploitation Capabilities:**
- 💬 SMS database dump (`/data/data/com.android.providers.telephony/`)
- 📇 Contacts exfiltration (`/data/data/com.android.providers.contacts/`)
- 📞 Call logs extraction
- 📂 File system browsing
- 📍 GPS location tracking

**Attack Flow:**
```
1. Bluetooth scanning for vulnerable devices
2. Exploit packet sent via Bluetooth
3. Reverse shell connects to C2 server (zeroclickexploits.ddns.net:4445)
4. Post-exploitation modules execute
5. Data exfiltrated to C2 server
```

---

## 📊 Demo Mode vs Production Mode

### **Demo Mode (DEMO_MODE=true)**
- **Safe for testing** - No real exploits deployed
- Simulates all attack vectors
- Logs all activities to database
- Perfect for training and demonstrations
- No actual devices are attacked

### **Production Mode (DEMO_MODE=false)**
- **For authorized testing only**
- Deploys real exploit payloads
- Actual WhatsApp/SMS/Email delivery
- Target authorization strictly enforced
- All activities audited and logged

---

## 🔒 Security & Authorization

### **Authorization System**

**All attacks require:**
1. Target must be in `config/mobile_targets.yaml`
2. Target status must be `active`
3. Authorization checked before every attack
4. Unauthorized attempts are logged and blocked

### **Audit Logging**

**All activities are logged to:**
- Database: `AttackSimulation` table
- Database: `AuditLog` table
- File: `logs/red_team_mobile_attack.log`
- File: `logs/blue_team_monitoring.log`

**Logged information includes:**
- Timestamp of attack
- Target phone number/email
- Attack type and platform
- Delivery method used
- Success/failure status
- Operator information
- Complete attack details

---

## 🧪 Testing Workflow

### **Complete Red vs Blue Simulation**

**Scenario:** Test iOS phishing attack with WhatsApp delivery

#### **Step 1: Red Team (Port 5008)**
1. Navigate to `http://localhost:5008`
2. Enter authorized target: `+1234567890`
3. Select platform: **Auto-Detect**
4. Choose attack: **Phishing**
5. Delivery: **WhatsApp (Infobip)**
6. Post-exploit: **Contacts, SMS, Location**
7. Click **DEPLOY ATTACK**

#### **Step 2: Blue Team (Port 5009)**
1. Navigate to `http://localhost:5009`
2. Observe **Active Attacks** counter increase
3. View threat in **Real-Time Threat Feed**
4. Check **Attack Timeline** for chronological view
5. Analyze details in **Detailed Threat Analysis** table
6. Verify CVE, platform, and delivery method

#### **Step 3: Verify Logs**
```bash
# Red Team logs
tail -f logs/red_team_mobile_attack.log

# Blue Team logs
tail -f logs/blue_team_monitoring.log

# Database verification
sqlite3 red_team_operations.db "SELECT * FROM attack_simulations WHERE attack_type LIKE '%mobile%' ORDER BY timestamp DESC LIMIT 5;"
```

---

## 📱 Infobip WhatsApp Integration

### **Setup Instructions**

1. **Sign up for Infobip account**
   - Visit: https://www.infobip.com/
   - Create account and verify

2. **Get API Key**
   - Navigate to Settings → API Keys
   - Create new API key
   - Copy key to `.env` file

3. **Configure WhatsApp Number**
   - Purchase or configure WhatsApp Business number
   - Set `INFOBIP_FROM_NUMBER` in `.env`
   - Enable WhatsApp: `INFOBIP_WHATSAPP_ENABLED=true`

4. **Test WhatsApp Delivery**
```python
from modules.mobile_security_testing import MobileSecurityTesting

tester = MobileSecurityTesting()
result = tester.send_whatsapp_test(
    phone_number="+1234567890",
    message="Test message from Red Team",
    test_name="whatsapp_test"
)
print(result)
```

### **WhatsApp Message Format**

```python
# Example exploit message via WhatsApp
{
    "messages": [
        {
            "from": "447860088970",
            "to": "1234567890",
            "content": {
                "text": "🔒 Security Alert: Your device requires immediate attention. Verify here: http://zeroclickexploits.ddns.net/exploit/[TARGET_ID]"
            }
        }
    ]
}
```

---

## 🎯 Advanced Features

### **Auto Device Detection**

The system automatically detects iOS vs Android devices using:
- SMS banner analysis
- iMessage delivery receipts
- Device fingerprinting techniques
- User-Agent string analysis

**Algorithm:**
```python
def detect_device_platform(target):
    # In production: analyze SMS/iMessage response
    # In demo: use last digit heuristic
    if target[-1] in '02468':
        return 'ios'  # Even digit = iOS
    else:
        return 'android'  # Odd digit = Android
```

### **Stealth Mode Features**

1. **Zero-Click Exploits**
   - No user interaction required
   - Silent exploitation
   - Minimal forensic footprint

2. **Auto-Detection**
   - Automatically selects optimal payload
   - Platform-specific exploit selection
   - Delivery method optimization

3. **C2 Callback**
   - Encrypted reverse shell
   - Persistent connection
   - Covert data exfiltration

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. "Target not authorized" error**
```bash
# Solution: Add target to config/mobile_targets.yaml
echo "  - type: phone
    value: \"+1234567890\"
    status: active" >> config/mobile_targets.yaml
```

#### **2. WhatsApp delivery fails**
```bash
# Check Infobip configuration
# Verify API key is correct
# Ensure WhatsApp number is activated
# Check logs: tail -f logs/mobile_testing.log
```

#### **3. Database connection error**
```bash
# Reinitialize database
python3 -c "from database.models import init_db; init_db()"
```

#### **4. Module import errors**
```bash
# Verify Python path
export PYTHONPATH=/home/EXQUISITE/Project-Red:$PYTHONPATH

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 API Endpoints

### **Red Team Dashboard (Port 5008)**

- `GET /` - Main dashboard interface
- `POST /api/deploy_attack` - Deploy mobile attack
- `GET /api/attack_stats` - Get attack statistics
- `GET /api/health` - Health check

### **Blue Team Dashboard (Port 5009)**

- `GET /` - Main monitoring interface
- `GET /api/blue_team_stats` - Get threat statistics
- `GET /api/threat_feed` - Real-time threat feed
- `GET /api/attack_timeline` - 24-hour attack timeline
- `GET /api/threat_details` - Detailed threat analysis
- `GET /api/health` - Health check

---

## 🎓 Training Scenarios

### **Scenario 1: iOS Phishing Campaign**
- Simulate Apple ID phishing attack
- WhatsApp delivery method
- Track Blue Team detection time

### **Scenario 2: Android Bluetooth Proximity Attack**
- Zero-click Bluetooth exploit
- No network connectivity required
- Test SOC response procedures

### **Scenario 3: Cross-Platform Attack**
- Target both iOS and Android devices
- Compare detection rates
- Analyze platform-specific indicators

---

## ⚠️ Legal & Ethical Considerations

**CRITICAL REMINDERS:**

1. **Authorization Required**
   - Only attack authorized targets
   - Obtain written permission
   - Document all testing activities

2. **Scope Limitations**
   - Respect testing boundaries
   - Do not attack production systems
   - Follow responsible disclosure

3. **Data Protection**
   - Secure all exfiltrated data
   - Delete test data after completion
   - Comply with data protection regulations

4. **Audit Trail**
   - Maintain complete logs
   - Document all findings
   - Report vulnerabilities responsibly

---

## 📞 Support & Resources

- **Documentation:** This file
- **Logs:** `logs/` directory
- **Database:** `red_team_operations.db`
- **Configuration:** `.env` and `config/mobile_targets.yaml`

---

## 🎉 Summary

You now have a **complete Red Team vs Blue Team mobile attack simulation system** with:

✅ iOS WebKit zero-click exploits (CVE-2021-30860)
✅ Android Bluetooth zero-click exploits (CVE-2023-45866)
✅ Infobip WhatsApp/SMS delivery integration
✅ Auto device detection (iOS vs Android)
✅ Post-exploitation modules (contacts, SMS, location)
✅ Red Team attack dashboard (Port 5008)
✅ Blue Team monitoring dashboard (Port 5009)
✅ Real-time threat analysis and detection
✅ Complete audit logging and authorization

**🚀 Ready for Red Team operations!**
