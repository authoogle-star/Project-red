# 📱 Mobile Security Testing Framework Guide

## Project Red Sword - iOS & Android Security Assessment

---

## 🎯 Overview

This mobile security testing framework integrates with Project Red Sword to provide comprehensive iOS and Android security assessments for **in-house team testing only**. The framework supports SMS and email-based attack simulations with full authorization controls and comprehensive logging.

### Key Features

- ✅ **iOS Testing**: Phishing, smishing, malicious profiles, WebKit tests
- ✅ **Android Testing**: Phishing, smishing, malicious APKs, Bluetooth tests
- ✅ **SMS Delivery**: Twilio integration for real SMS testing
- ✅ **Email Delivery**: SendGrid integration for real email testing
- ✅ **Authorization Controls**: Whitelist-based target authorization
- ✅ **Demo Mode**: Safe simulation without real delivery
- ✅ **Comprehensive Logging**: Database + audit trails
- ✅ **Web C2 Panel**: Real-time command & control interface
- ✅ **Statistics Dashboard**: Live testing metrics

---

## 🚀 Quick Start

### Step 1: Configure Authorized Targets

Edit `config/mobile_targets.yaml` and add your in-house team members' devices:

```yaml
authorized_targets:
  - type: phone
    value: "+15555551234"  # Replace with actual number
    device_type: ios
    device_name: "Test iPhone - Security Team"
    owner: "team_member_name"
    status: active
    authorized_by: "security_director"
    authorization_date: "2024-01-01"
```

### Step 2: Start the Mobile Testing C2 Panel

```bash
cd /home/EXQUISITE/Project-Red-Sword
./scripts/start_mobile_testing.sh
```

### Step 3: Access the Web Interface

Open your browser to: **http://localhost:5007**

### Step 4: Run Your First Test

1. In the web interface, select "SMS Security Testing"
2. Enter an authorized phone number from your config
3. Choose a test type (e.g., "Phishing/Smishing Test")
4. Click "Send SMS Test"
5. Check logs: `tail -f logs/mobile_testing.log`

---

## 🔧 Configuration

### Demo Mode vs Live Mode

#### Demo Mode (Default - Safe Testing)

```bash
# In .env file
DEMO_MODE=true
MOBILE_TESTING_DEMO_MODE=true
```

**What happens:**
- ✅ No real SMS sent (simulated)
- ✅ No real emails sent (simulated)
- ✅ All actions logged
- ✅ Safe for testing the framework

#### Live Mode (Real Testing)

```bash
# In .env file
DEMO_MODE=false
MOBILE_TESTING_DEMO_MODE=false
```

**Requirements:**
- Twilio account for SMS delivery
- SendGrid account for email delivery
- Proper credentials configured

---

## 📧 Setting Up Real SMS/Email Delivery

### Twilio Setup (SMS)

1. **Create Account**: https://www.twilio.com/try-twilio
   - Free tier: 100 SMS/month

2. **Get Credentials**:
   - Account SID
   - Auth Token
   - Phone Number

3. **Add to .env**:
```bash
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### SendGrid Setup (Email)

1. **Create Account**: https://signup.sendgrid.com
   - Free tier: 100 emails/day

2. **Get API Key**:
   - Settings → API Keys → Create API Key
   - Full Access permissions

3. **Add to .env**:
```bash
SENDGRID_API_KEY=your_api_key_here
SENDGRID_FROM_EMAIL=security-testing@yourcompany.com
```

---

## 🎯 Testing Scenarios

### Phishing Email Test

**Scenario**: Test if team members can identify phishing emails

```
1. Navigate to "Email Security Testing" section
2. Enter authorized email address
3. Select platform (iOS or Android)
4. Choose "Phishing Email" test type
5. Customize subject and message
6. Send test
7. Monitor if recipient clicks/reports
```

### SMS Phishing (Smishing) Test

**Scenario**: Test if team members can identify SMS phishing

```
1. Navigate to "SMS Security Testing" section
2. Enter authorized phone number
3. Select "Phishing/Smishing Test"
4. Customize message (e.g., fake package delivery)
5. Send test
6. Track if recipient clicks link or reports suspicious SMS
```

### Mobile Deployment Test

**Scenario**: Full mobile security assessment

```
1. Navigate to "Mobile Test Deployment" section
2. Enter target (phone or email)
3. Select platform (iOS/Android)
4. Choose test type:
   - Phishing
   - Smishing
   - Malicious Profile (iOS)
   - Malicious APK (Android)
5. Deploy test
6. Monitor results in logs and dashboard
```

---

## 🛡️ Safety Controls

### Authorization System

**Only authorized targets can be tested:**

```yaml
# config/mobile_targets.yaml
authorized_targets:
  - type: phone
    value: "+15555551234"
    status: active  # or 'inactive' to disable
```

**If target is not authorized:**
- ❌ Test is blocked
- 📝 Attempt is logged to audit trail
- ⚠️ Warning displayed to operator

### Rate Limiting

```yaml
# config/mobile_targets.yaml
safety:
  max_tests_per_target_per_day: 10
  max_concurrent_tests: 5
  test_window:
    start_hour: 9  # 9 AM
    end_hour: 17   # 5 PM
```

### Audit Trail

All activities are logged to:
- **Database**: `red_team_operations.db` (attack_simulations, audit_log tables)
- **Log File**: `logs/mobile_testing.log`
- **C2 Log**: `logs/mobile_c2.log`

---

## 📊 Monitoring & Reporting

### Real-Time Statistics

The C2 panel displays:
- **Total Tests**: Number of tests conducted
- **Successful Tests**: Tests delivered successfully
- **Success Rate**: Percentage of successful deliveries
- **Authorized Targets**: Number of configured targets

### Database Queries

```bash
# View recent mobile tests
sqlite3 red_team_operations.db "
SELECT attack_type, target, status, timestamp
FROM attack_simulations
WHERE attack_type LIKE 'mobile_testing_%'
ORDER BY timestamp DESC
LIMIT 10;
"

# View audit trail
sqlite3 red_team_operations.db "
SELECT action, target, timestamp, details
FROM audit_log
WHERE action LIKE 'MOBILE_TEST_%'
ORDER BY timestamp DESC
LIMIT 10;
"
```

### Log Files

```bash
# Real-time mobile testing logs
tail -f logs/mobile_testing.log

# Real-time C2 panel logs
tail -f logs/mobile_c2.log

# All attack simulations
tail -f logs/attack_simulation.log
```

---

## 🔌 API Endpoints

The C2 panel exposes REST APIs for integration:

### Get Statistics
```bash
curl http://localhost:5007/api/stats
```

### Send SMS Test
```bash
curl -X POST http://localhost:5007/api/sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+15555551234",
    "message": "Security test message",
    "test_name": "Smishing Test"
  }'
```

### Send Email Test
```bash
curl -X POST http://localhost:5007/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "email_address": "test@company.com",
    "subject": "Security Test",
    "message": "Test message",
    "test_name": "Phishing Test"
  }'
```

### Deploy Mobile Test
```bash
curl -X POST http://localhost:5007/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "target": "+15555551234",
    "platform": "ios",
    "test_type": "phishing"
  }'
```

### Health Check
```bash
curl http://localhost:5007/api/health
```

---

## 🔬 Integration with Existing Infrastructure

### Email Server Integration

The mobile testing framework uses:
- **Existing EmailServer**: `core/email_server/EmailServer.py`
- **Email Handler**: `core/integrations/email_handler.py`
- **SendGrid**: For external email delivery

### Database Integration

Uses existing Project Red Sword database:
- **AttackSimulation** table: Records all mobile tests
- **AuditLog** table: Immutable audit trail
- **SessionLocal**: Database session management

### Dashboard Integration

Access mobile testing from main dashboard:
- Main Red Team Dashboard: http://localhost:5006/red_team_dashboard
- Mobile Testing C2 Panel: http://localhost:5007

---

## 📋 Red Team vs Blue Team Exercises

### Exercise Configuration

Edit `config/mobile_targets.yaml`:

```yaml
exercise_config:
  current_exercise: "Mobile Security Assessment Q1 2024"
  exercise_name: "Mobile Security Assessment 2024"
  start_date: "2024-01-15"
  end_date: "2024-01-19"
  red_team_members:
    - "red_team_operator_1"
    - "red_team_operator_2"
  blue_team_members:
    - "blue_team_analyst_1"
    - "blue_team_analyst_2"
  notification_email: "security-team@yourcompany.com"
```

### Exercise Workflow

1. **Planning**:
   - Configure authorized targets (in-house team devices)
   - Set exercise dates
   - Brief red/blue teams

2. **Execution** (Red Team):
   - Launch mobile tests via C2 panel
   - Track delivery success rates
   - Document attack vectors used

3. **Detection** (Blue Team):
   - Monitor for suspicious SMS/emails
   - Test incident response procedures
   - Document detection capabilities

4. **Analysis**:
   - Review logs and statistics
   - Identify gaps in detection
   - Generate improvement recommendations

---

## 🎓 Testing Best Practices

### DO:
✅ Only test authorized in-house team devices
✅ Get explicit written authorization before testing
✅ Start with demo mode to understand the system
✅ Configure authorized targets properly
✅ Monitor logs in real-time during tests
✅ Document all testing activities
✅ Conduct tests during business hours (respecting test_window)
✅ Debrief team members after tests

### DON'T:
❌ Test unauthorized devices or external numbers
❌ Send real malware or exploits
❌ Conduct tests without proper authorization
❌ Ignore safety controls or rate limits
❌ Test outside approved time windows
❌ Skip documentation and reporting
❌ Use real exploits from mobile-click-testing.txt without proper controls

---

## 🚨 Troubleshooting

### Problem: "Target not authorized for testing"

**Solution**: Add target to `config/mobile_targets.yaml` with `status: active`

### Problem: SMS not sending (Live Mode)

**Check**:
1. Twilio credentials in `.env` are correct
2. `DEMO_MODE=false` in `.env`
3. Phone number format is correct (+1234567890)
4. Twilio account has credits
5. Check logs: `tail -f logs/mobile_testing.log`

### Problem: Email not sending (Live Mode)

**Check**:
1. SendGrid API key in `.env` is correct
2. `DEMO_MODE=false` in `.env`
3. From email is verified in SendGrid
4. Check logs: `tail -f logs/mobile_testing.log`

### Problem: C2 Panel not loading

**Check**:
1. Port 5007 is not in use: `lsof -i :5007`
2. Virtual environment is activated
3. Dependencies installed: `pip install -r requirements.txt`
4. Check C2 logs: `tail -f logs/mobile_c2.log`

### Problem: Database errors

**Solution**:
```bash
python3 -c "from database.models import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## 📁 File Structure

```
Project-Red-Sword/
├── modules/
│   └── mobile_security_testing.py    # Mobile testing module
├── config/
│   └── mobile_targets.yaml           # Authorized targets config
├── scripts/
│   └── start_mobile_testing.sh       # C2 startup script
├── mobile_testing_c2_panel.py        # Flask C2 web interface
├── logs/
│   ├── mobile_testing.log            # Mobile test logs
│   └── mobile_c2.log                 # C2 panel logs
├── .env                              # Environment configuration
├── requirements.txt                  # Python dependencies
└── MOBILE_TESTING_GUIDE.md          # This file
```

---

## 🔐 Security Considerations

### Authorization

- All tests require explicit authorization
- Targets must be listed in `mobile_targets.yaml`
- Unauthorized attempts are logged and blocked

### Logging & Auditing

- All activities logged to database
- Immutable audit trail
- Operator identification
- Timestamp tracking

### Data Protection

- Test messages should not contain real credentials
- Use placeholder data for testing
- Sanitize logs before sharing
- Follow company data protection policies

### Legal Compliance

- Only test company-owned devices
- Get written authorization
- Follow local telecommunications laws
- Respect privacy regulations

---

## 📞 Support & Contact

For questions or issues:
- Check logs: `logs/mobile_testing.log`
- Review this guide
- Contact security team lead
- Reference: `docs/mobile-click-testing.txt`

---

## 🎯 Summary

The Mobile Security Testing Framework provides a complete solution for assessing your in-house team's mobile security awareness. Key capabilities:

1. **SMS Testing**: Twilio-powered SMS delivery
2. **Email Testing**: SendGrid-powered email delivery
3. **Web C2 Panel**: Real-time command & control
4. **Authorization**: Whitelist-based targeting
5. **Logging**: Comprehensive audit trails
6. **Demo Mode**: Safe simulation testing
7. **Statistics**: Real-time metrics dashboard

**Remember**: This is for **in-house testing only**. Always get proper authorization before conducting security tests.

---

**Happy (Authorized) Testing! 🛡️**
