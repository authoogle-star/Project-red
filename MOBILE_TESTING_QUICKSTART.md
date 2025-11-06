# 🚀 Mobile Testing - Quick Start Guide

## 📱 What Was Built

A complete **mobile security testing framework** for iOS and Android, integrated with your existing Project Red Sword infrastructure.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Project Red Sword                          │
│                                                             │
│  ┌─────────────────┐         ┌──────────────────┐        │
│  │  Main Dashboard │         │  Mobile Testing  │        │
│  │   Port 5006     │────────▶│   C2 Panel       │        │
│  └─────────────────┘         │   Port 5007      │        │
│                               └──────────────────┘        │
│                                        │                   │
│                      ┌─────────────────┴────────────────┐ │
│                      │                                   │ │
│              ┌───────▼─────────┐           ┌────────▼───────┐
│              │  SMS Delivery   │           │ Email Delivery │
│              │   (Twilio)      │           │  (SendGrid)    │
│              └───────┬─────────┘           └────────┬───────┘
│                      │                              │       │
│              ┌───────▼──────────────────────────────▼─────┐ │
│              │     Authorization & Logging System         │ │
│              │  (mobile_targets.yaml + Database)          │ │
│              └────────────────────────────────────────────┘ │
│                                                             │
│  Target Devices:                                           │
│  ┌────────────┐                    ┌────────────┐         │
│  │  iOS       │                    │  Android   │         │
│  │  Devices   │                    │  Devices   │         │
│  └────────────┘                    └────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 What's Included

### 1. **Mobile Security Testing Module**
- **File**: `modules/mobile_security_testing.py`
- **Purpose**: Core Python module for SMS/email testing
- **Features**:
  - Target authorization validation
  - SMS delivery via Twilio
  - Email delivery via SendGrid
  - Demo mode for safe testing
  - Comprehensive logging

### 2. **Flask C2 Web Panel**
- **File**: `mobile_testing_c2_panel.py`
- **Purpose**: Real-time command & control interface
- **Access**: http://localhost:5007
- **Features**:
  - Web-based testing interface
  - Real-time statistics dashboard
  - Activity log monitoring
  - REST API endpoints

### 3. **Configuration Files**
- **Targets**: `config/mobile_targets.yaml`
  - Authorized device whitelist
  - Team member assignments
  - Exercise configuration

- **Environment**: `.env`
  - Twilio credentials
  - SendGrid credentials
  - Demo mode toggle

### 4. **Startup Script**
- **File**: `scripts/start_mobile_testing.sh`
- **Purpose**: Automated C2 panel startup
- **Checks**: Dependencies, config, database

### 5. **Documentation**
- **Guide**: `MOBILE_TESTING_GUIDE.md` (comprehensive)
- **Quick Start**: `MOBILE_TESTING_QUICKSTART.md` (this file)

---

## 🎯 Two Modes of Operation

### Mode 1: Demo Mode (Safe - Default)

**Perfect for:**
- Learning the system
- Testing the framework
- No real SMS/emails sent

**How to use:**
```bash
# .env should have:
DEMO_MODE=true
MOBILE_TESTING_DEMO_MODE=true

# Start the C2 panel
./scripts/start_mobile_testing.sh

# Access: http://localhost:5007
# All tests will be simulated and logged
```

### Mode 2: Live Mode (Real Testing)

**Perfect for:**
- Actual red team exercises
- Real mobile security testing
- In-house team assessments

**How to use:**
```bash
# Step 1: Get API credentials
# - Twilio: https://www.twilio.com (100 SMS/month free)
# - SendGrid: https://sendgrid.com (100 emails/day free)

# Step 2: Add to .env
DEMO_MODE=false
MOBILE_TESTING_DEMO_MODE=false
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1234567890
SENDGRID_API_KEY=your_api_key_here

# Step 3: Configure authorized targets
# Edit config/mobile_targets.yaml

# Step 4: Start testing
./scripts/start_mobile_testing.sh
```

---

## 🎬 Your First Mobile Test (5 Minutes)

### Step 1: Configure a Test Target (2 min)

Edit `config/mobile_targets.yaml`:

```yaml
authorized_targets:
  - type: phone
    value: "+15555551234"  # YOUR actual in-house team phone
    device_type: ios
    device_name: "Test iPhone - Your Name"
    owner: "your_name"
    status: active
    authorized_by: "security_director"
    authorization_date: "2024-01-01"
```

### Step 2: Start the C2 Panel (1 min)

```bash
cd /home/EXQUISITE/Project-Red-Sword
./scripts/start_mobile_testing.sh
```

### Step 3: Run a Test (2 min)

1. Open browser: http://localhost:5007
2. Scroll to "SMS Security Testing" section
3. Enter your authorized phone: `+15555551234`
4. Select test type: "Phishing/Smishing Test"
5. Message: "Your package delivery failed. Click here: [TEST]"
6. Click "Send SMS Test"
7. **In Demo Mode**: Check logs to see simulation
   **In Live Mode**: Check your phone for real SMS

### Step 4: Check Results (instant)

Look at the **Statistics Dashboard** at top of page:
- Total Tests: 1
- Successful Tests: 1
- Success Rate: 100%

Check logs:
```bash
tail -f logs/mobile_testing.log
```

**Done!** You just ran your first mobile security test! 🎉

---

## 🔥 Common Test Scenarios

### Scenario 1: SMS Phishing Test

**Goal**: Test if team members identify fake delivery SMS

```
1. C2 Panel → SMS Security Testing
2. Phone: +15555551234
3. Type: Phishing/Smishing Test
4. Message: "FedEx: Package delivery failed. Reschedule: http://test-link.com"
5. Send Test
6. Monitor: Did recipient click? Did they report it?
```

### Scenario 2: Email Phishing Test

**Goal**: Test if team members identify fake security emails

```
1. C2 Panel → Email Security Testing
2. Email: test@yourcompany.com
3. Platform: iOS
4. Type: Phishing Email
5. Subject: "Urgent: Account Security Alert"
6. Body: "Your account has been compromised. Click here to secure it."
7. Send Test
8. Monitor: Did recipient click? Did they report it?
```

### Scenario 3: Full Mobile Deployment

**Goal**: Comprehensive mobile security assessment

```
1. C2 Panel → Mobile Test Deployment
2. Target: +15555551234 (or email)
3. Platform: iOS or Android
4. Test Type: phishing, smishing, malicious_profile, or malicious_apk
5. Deploy Test
6. Results: Check logs and statistics
```

---

## 📊 Monitoring & Reporting

### Real-Time Monitoring

**Web Dashboard**: http://localhost:5007
- Live statistics
- Activity log
- Success rates

**Log Files**:
```bash
# Mobile testing logs
tail -f logs/mobile_testing.log

# C2 panel logs
tail -f logs/mobile_c2.log

# All system logs
tail -f logs/attack_simulation.log
```

### Database Queries

```bash
# Recent mobile tests
sqlite3 red_team_operations.db "
SELECT attack_type, target, status, timestamp
FROM attack_simulations
WHERE attack_type LIKE 'mobile_testing_%'
ORDER BY timestamp DESC LIMIT 10;
"

# Test statistics
sqlite3 red_team_operations.db "
SELECT
  attack_type,
  COUNT(*) as total,
  SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) as successful
FROM attack_simulations
WHERE attack_type LIKE 'mobile_testing_%'
GROUP BY attack_type;
"
```

---

## 🔌 REST API Usage

### Using cURL

```bash
# Get statistics
curl http://localhost:5007/api/stats

# Send SMS test
curl -X POST http://localhost:5007/api/sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+15555551234",
    "message": "Test message",
    "test_name": "API Test"
  }'

# Send email test
curl -X POST http://localhost:5007/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "email_address": "test@company.com",
    "subject": "Test",
    "message": "Test email",
    "test_name": "API Test"
  }'

# Deploy mobile test
curl -X POST http://localhost:5007/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "target": "+15555551234",
    "platform": "ios",
    "test_type": "phishing"
  }'
```

### Using Python

```python
import requests

# Send SMS test
response = requests.post('http://localhost:5007/api/sms', json={
    'phone_number': '+15555551234',
    'message': 'Security test message',
    'test_name': 'Python API Test'
})
print(response.json())

# Get statistics
stats = requests.get('http://localhost:5007/api/stats').json()
print(f"Total tests: {stats['total_tests']}")
print(f"Success rate: {stats['success_rate']}%")
```

---

## 🛡️ Safety Controls

### Authorization System

**All tests require authorization:**

✅ **Authorized Target** = Test proceeds + logged
❌ **Unauthorized Target** = Test blocked + logged as violation

### Rate Limiting

Configured in `config/mobile_targets.yaml`:
- Max 10 tests per target per day
- Max 5 concurrent tests
- Test window: 9 AM - 5 PM

### Audit Trail

Every action logged to:
1. **Database**: Immutable audit log
2. **Log Files**: Time-stamped entries
3. **Statistics**: Real-time counters

---

## 📱 Integration with Main Dashboard

The mobile testing framework is now integrated with your main Red Team dashboard:

**Main Dashboard**: http://localhost:5006/red_team_dashboard
- New section: "Mobile Security Testing"
- Link to Mobile C2 Panel
- Quick start instructions

**Mobile C2 Panel**: http://localhost:5007
- Dedicated mobile testing interface
- Real-time operations
- Independent logging

**Run Both**:
```bash
# Terminal 1: Main dashboard
./scripts/start_red_team.sh

# Terminal 2: Mobile C2 panel
./scripts/start_mobile_testing.sh
```

---

## 🎓 Red Team Exercise Example

### Scenario: Quarterly Mobile Security Assessment

**Goal**: Test in-house team's ability to detect mobile threats

#### Phase 1: Planning (Day 1)

```bash
# 1. Configure targets
vim config/mobile_targets.yaml
# Add all in-house team member devices

# 2. Configure exercise
exercise_config:
  exercise_name: "Q1 2024 Mobile Security Assessment"
  start_date: "2024-01-15"
  end_date: "2024-01-19"
```

#### Phase 2: Execution (Days 2-4)

```bash
# Start C2 panel
./scripts/start_mobile_testing.sh

# Day 2: SMS Phishing
# - Target: All iOS devices
# - Type: Package delivery scam
# - Monitor: Click rates

# Day 3: Email Phishing
# - Target: All Android devices
# - Type: Fake security alert
# - Monitor: Credential harvesting attempts

# Day 4: Mixed Attacks
# - Target: Random selection
# - Type: Various attack vectors
# - Monitor: Detection and reporting
```

#### Phase 3: Analysis (Day 5)

```bash
# Generate statistics
sqlite3 red_team_operations.db "
SELECT
  device_type,
  test_type,
  COUNT(*) as total_tests,
  SUM(CASE WHEN clicked='true' THEN 1 ELSE 0 END) as clicked,
  SUM(CASE WHEN reported='true' THEN 1 ELSE 0 END) as reported
FROM mobile_test_results
GROUP BY device_type, test_type;
"

# Findings:
# - Click rate: 35% (target: <20%)
# - Report rate: 15% (target: >50%)
# - Recommendation: More security awareness training
```

---

## 🚨 Troubleshooting

### Issue: "Target not authorized"

**Fix**: Add to `config/mobile_targets.yaml` with `status: active`

### Issue: SMS not sending (Live Mode)

**Check**:
```bash
# 1. Demo mode disabled?
grep "DEMO_MODE" .env
# Should be: DEMO_MODE=false

# 2. Twilio configured?
grep "TWILIO" .env
# Should have all 3 credentials

# 3. Check logs
tail -f logs/mobile_testing.log
```

### Issue: C2 Panel won't start

**Fix**:
```bash
# Check port available
lsof -i :5007

# Kill existing process
kill $(lsof -t -i:5007)

# Reinstall dependencies
pip install -r requirements.txt

# Try again
./scripts/start_mobile_testing.sh
```

---

## 📚 Full Documentation

For complete details, see:
- **Comprehensive Guide**: `MOBILE_TESTING_GUIDE.md`
- **Original Spec**: `docs/mobile-click-testing.txt`
- **Main Dashboard Guide**: `PRODUCTION_DEPLOYMENT_GUIDE.md`

---

## ✅ Next Steps

1. **Try Demo Mode**:
   ```bash
   ./scripts/start_mobile_testing.sh
   # Access: http://localhost:5007
   ```

2. **Configure Authorized Targets**:
   ```bash
   vim config/mobile_targets.yaml
   ```

3. **Get API Credentials** (for Live Mode):
   - Twilio: https://www.twilio.com
   - SendGrid: https://sendgrid.com

4. **Run Your First Exercise**:
   - Plan targets
   - Execute tests
   - Analyze results
   - Generate report

5. **Integrate with Blue Team**:
   - Share findings
   - Improve detection
   - Update response procedures

---

## 🎉 Summary

You now have a **production-ready mobile security testing framework** that:

✅ Tests iOS and Android devices
✅ Sends real SMS via Twilio
✅ Sends real emails via SendGrid
✅ Enforces authorization controls
✅ Provides real-time web interface
✅ Logs all activities
✅ Integrates with Project Red Sword
✅ Supports red team vs blue team exercises

**Ready to test your team's mobile security!** 🛡️📱

---

**Questions?** Check `MOBILE_TESTING_GUIDE.md` for detailed answers.
