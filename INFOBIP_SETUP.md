# Infobip SMS & WhatsApp Setup Guide

## Overview

This guide will help you configure Infobip as the SMS and WhatsApp provider for Project Red Sword mobile security testing.

**Infobip** provides enterprise-grade SMS and WhatsApp messaging APIs with:
- Global SMS delivery
- WhatsApp Business API
- High deliverability rates
- Detailed analytics and reporting
- Competitive pricing

---

## Prerequisites

- Active Infobip account
- API key from Infobip dashboard
- WhatsApp Business account (for WhatsApp testing)
- Approved WhatsApp templates (for template messages)

---

## Step 1: Create Infobip Account

1. **Sign up** at https://www.infobip.com/signup

2. **Verify your account** via email

3. **Complete account setup**:
   - Business information
   - Payment method (if using paid tier)
   - Phone number verification

---

## Step 2: Get API Credentials

1. **Login to Infobip Portal**: https://portal.infobip.com

2. **Navigate to API Keys**:
   - Go to `Settings` → `API Keys`
   - Click `Create API Key`

3. **Create API Key**:
   - Name: `Project Red Sword - Mobile Testing`
   - Permissions: `SMS` and `WhatsApp` (if using WhatsApp)
   - Click `Generate`

4. **Copy your API Key**:
   - Format: `App [long-string-here]`
   - Example: `App 50c89af57305b3b7fb2fad8107d1cc03-ba87bbca-b537-4225-814d-aac8aef3d4a0`
   - **Save this securely** - it won't be shown again!

5. **Note your Base URL**:
   - Found in API documentation
   - Example: `https://g9vm5e.api.infobip.com`
   - This varies by region

---

## Step 3: Configure Sender Number

### For SMS:

1. **Get a Sender ID**:
   - Go to `SMS` → `Sender Names`
   - Request a sender number or alphanumeric ID
   - Wait for approval (1-2 business days)

2. **Test Number** (for development):
   - Use Infobip's test numbers
   - Example: `447860088970`

### For WhatsApp:

1. **Register WhatsApp Business Account**:
   - Go to `WhatsApp` → `Sender Registration`
   - Follow Facebook Business verification
   - Link your phone number

2. **Create Message Templates**:
   - Go to `WhatsApp` → `Message Templates`
   - Create and submit templates for approval
   - Example: `test_whatsapp_template_en`

---

## Step 4: Configure Project Red Sword

### Update `.env` File

Create or update your `.env` file with Infobip credentials:

```bash
# Mobile Testing Configuration
DEMO_MODE=false  # Set to false for real SMS delivery

# SMS Provider Selection
SMS_PROVIDER=infobip  # Use 'infobip' or 'textbelt'

# Infobip API Configuration
INFOBIP_API_KEY=App 50c89af57305b3b7fb2fad8107d1cc03-ba87bbca-b537-4225-814d-aac8aef3d4a0
INFOBIP_BASE_URL=https://g9vm5e.api.infobip.com
INFOBIP_FROM_NUMBER=447860088970
INFOBIP_WHATSAPP_ENABLED=true
```

### Configuration Options

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `INFOBIP_API_KEY` | Your Infobip API key | Yes | `App xxx-xxx-xxx` |
| `INFOBIP_BASE_URL` | API endpoint URL | Yes | `https://g9vm5e.api.infobip.com` |
| `INFOBIP_FROM_NUMBER` | Sender phone number | Yes | `447860088970` |
| `INFOBIP_WHATSAPP_ENABLED` | Enable WhatsApp testing | No | `true` or `false` |
| `SMS_PROVIDER` | SMS provider to use | No | `infobip` or `textbelt` |
| `DEMO_MODE` | Simulate vs real delivery | No | `true` or `false` |

---

## Step 5: Test SMS Delivery

### Test via Python

```python
from modules.mobile_security_testing import MobileSecurityTesting

# Initialize mobile tester
mobile = MobileSecurityTesting()

# Send test SMS
result = mobile.send_sms_test(
    phone_number="+12164341828",
    message="This is a security test SMS from Project Red Sword",
    test_name="Infobip Test"
)

print(f"Success: {result['success']}")
print(f"Provider: {result.get('provider')}")
print(f"Message ID: {result.get('message_id')}")
```

### Test via Dashboard

1. **Open dashboard**: http://localhost:5006/red_team_dashboard

2. **Go to Mobile Testing tab**

3. **Configure test**:
   - Select device type: iOS or Android
   - Enter authorized phone number
   - Choose test type: Smishing
   - Enter custom message

4. **Click "📱 Send SMS Test"**

5. **Check logs**:
   ```bash
   tail -f logs/mobile_testing.log
   ```

### Test via C2 Panel

1. **Start C2 panel**:
   ```bash
   ./scripts/start_mobile_testing.sh
   ```

2. **Open panel**: http://localhost:5007

3. **Send SMS test** through the web interface

---

## Step 6: Test WhatsApp Delivery

### Prerequisites for WhatsApp

- WhatsApp Business account linked to Infobip
- Approved message templates
- Recipient phone number registered with WhatsApp

### Test via Python

```python
from modules.mobile_security_testing import MobileSecurityTesting

# Initialize mobile tester
mobile = MobileSecurityTesting()

# Send WhatsApp test (template message)
result = mobile.send_whatsapp_test(
    phone_number="+12164341828",
    message="john",  # Template placeholder value
    test_name="WhatsApp Template Test",
    template_name="test_whatsapp_template_en"
)

print(f"Success: {result['success']}")
print(f"Message ID: {result.get('message_id')}")
```

### WhatsApp Template Message Example

The code you provided sends a template message:

```python
import http.client
import json

conn = http.client.HTTPSConnection("g9vm5e.api.infobip.com")
payload = json.dumps({
    "messages": [
        {
            "from": "447860088970",
            "to": "12164341828",
            "messageId": "a5f77a90-3da5-4930-a6ba-e3903751f63f",
            "content": {
                "templateName": "test_whatsapp_template_en",
                "templateData": {
                    "body": {
                        "placeholders": ["john"]
                    }
                },
                "language": "en"
            }
        }
    ]
})
headers = {
    'Authorization': 'App 50c89af57305b3b7fb2fad8107d1cc03-ba87bbca-b537-4225-814d-aac8aef3d4a0',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
conn.request("POST", "/whatsapp/1/message/template", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

This functionality is now integrated into Project Red Sword!

---

## API Endpoints Used

### SMS Endpoint

```
POST /sms/2/text/advanced
```

**Payload**:
```json
{
  "messages": [
    {
      "from": "447860088970",
      "to": "12164341828",
      "text": "Your security test message"
    }
  ]
}
```

### WhatsApp Template Endpoint

```
POST /whatsapp/1/message/template
```

**Payload**:
```json
{
  "messages": [
    {
      "from": "447860088970",
      "to": "12164341828",
      "content": {
        "templateName": "test_whatsapp_template_en",
        "templateData": {
          "body": {
            "placeholders": ["value1", "value2"]
          }
        },
        "language": "en"
      }
    }
  ]
}
```

### WhatsApp Text Endpoint

```
POST /whatsapp/1/message/text
```

**Payload**:
```json
{
  "messages": [
    {
      "from": "447860088970",
      "to": "12164341828",
      "content": {
        "text": "Your message text"
      }
    }
  ]
}
```

---

## Pricing

### SMS Pricing

- **Pay-as-you-go**: Varies by destination country
- **US SMS**: ~$0.0075 per message
- **UK SMS**: ~$0.045 per message
- **Free trial**: Credits available for new accounts

### WhatsApp Pricing

- **User-initiated conversations**: Free
- **Business-initiated conversations**: ~$0.005 - $0.04 per message
- **Template messages**: Required for business-initiated

### Check Current Pricing

Visit: https://www.infobip.com/pricing

---

## Monitoring & Logs

### View Delivery Status

1. **Infobip Portal**:
   - Go to `Analytics` → `Message Logs`
   - Filter by date, status, sender
   - Export reports

2. **Project Red Sword Logs**:
   ```bash
   tail -f logs/mobile_testing.log
   ```

3. **Database Logs**:
   ```bash
   sqlite3 red_team_operations.db "
   SELECT * FROM attack_simulations
   WHERE attack_type LIKE 'mobile_testing_%'
   ORDER BY timestamp DESC LIMIT 10;
   "
   ```

---

## Troubleshooting

### Issue: API Authentication Failed

**Error**: `401 Unauthorized`

**Solution**:
- Verify API key is correct in `.env`
- Ensure API key has SMS/WhatsApp permissions
- Check API key hasn't been revoked

### Issue: Message Not Delivered

**Error**: `Invalid destination`

**Solution**:
- Phone number must be in E.164 format: `+12164341828`
- No spaces, dashes, or parentheses
- Include country code with `+`

### Issue: WhatsApp Template Not Found

**Error**: `Template not found`

**Solution**:
- Verify template is approved in Infobip portal
- Check template name matches exactly
- Ensure template language is correct

### Issue: Rate Limiting

**Error**: `Too many requests`

**Solution**:
- Check rate limits in Infobip portal
- Implement delays between messages
- Upgrade plan for higher limits

---

## Security Best Practices

1. **Protect API Keys**:
   - Never commit `.env` to git
   - Use environment variables in production
   - Rotate keys regularly

2. **Authorization Controls**:
   - Only test authorized targets
   - Maintain `config/mobile_targets.yaml`
   - Log all activities

3. **Demo Mode**:
   - Use `DEMO_MODE=true` for testing
   - Verify configuration before going live
   - Test with personal devices first

4. **Monitoring**:
   - Review delivery logs regularly
   - Monitor for unauthorized use
   - Set up alerts for failures

---

## Support

### Infobip Support

- **Documentation**: https://www.infobip.com/docs
- **Support Portal**: https://www.infobip.com/contact
- **Email**: support@infobip.com
- **Knowledge Base**: https://www.infobip.com/docs/api

### Project Red Sword

- **Documentation**: See `MOBILE_TESTING_GUIDE.md`
- **Issues**: Report via project maintainer

---

## Next Steps

1. ✅ Configure Infobip API credentials
2. ✅ Test SMS delivery
3. ✅ Test WhatsApp delivery (if enabled)
4. ✅ Configure authorized targets in `config/mobile_targets.yaml`
5. ✅ Set up monitoring and logging
6. ✅ Review security practices
7. ✅ Start mobile security testing!

---

## Quick Reference

### Send SMS via Infobip

```python
from modules.mobile_security_testing import MobileSecurityTesting
mobile = MobileSecurityTesting()
result = mobile.send_sms_test("+12164341828", "Test message", "Test")
```

### Send WhatsApp via Infobip

```python
from modules.mobile_security_testing import MobileSecurityTesting
mobile = MobileSecurityTesting()
result = mobile.send_whatsapp_test("+12164341828", "Test message", "Test")
```

### Check Configuration

```python
from modules.mobile_security_testing import MobileSecurityTesting
mobile = MobileSecurityTesting()
print(f"Provider: {mobile.sms_provider}")
print(f"WhatsApp: {mobile.infobip_whatsapp_enabled}")
print(f"Demo Mode: {mobile.demo_mode}")
```

---

**Last Updated**: 2025-11-05
**Version**: 1.0
