# 📱 TextBelt SMS Integration Guide

## What is TextBelt?

TextBelt is a simple SMS API for sending text messages. It's **much simpler** than Twilio - no account signup required for basic testing!

**Website**: https://textbelt.com

---

## 🆓 Free Tier

TextBelt offers a **free tier** with no signup required:

- **API Key**: `textbelt` (built-in)
- **Limit**: 1 text message per day per phone number
- **Perfect for**: Testing and development

---

## 💰 Paid Tier (Optional)

For production red team exercises:

- **Cost**: $0.0064 per message (less than 1 cent!)
- **Purchase**: https://textbelt.com/purchase
- **No monthly fees**: Pay only for what you use
- **Get API key**: After purchase, you'll receive your API key

---

## ⚙️ Configuration

### Using Free Tier (Default - Already Configured!)

Your `.env` file is already set up for free tier:

```bash
TEXTBELT_API_KEY=textbelt
```

**No changes needed!** This works out of the box.

### Using Paid Tier (For Production)

If you purchased an API key:

```bash
# Edit .env file
TEXTBELT_API_KEY=your_purchased_api_key_here
```

---

## 🚀 How It Works

### Free Tier Behavior

```python
# Sends 1 SMS per day per number
phone_number = "+15555551234"
message = "Security test message"

# First message of the day: ✓ SENT
# Second message of the day: ✗ QUOTA EXCEEDED (wait 24 hours)
```

### Paid Tier Behavior

```python
# Unlimited messages with your API key
TEXTBELT_API_KEY=your_key_here

# Message 1: ✓ SENT
# Message 2: ✓ SENT
# Message 3: ✓ SENT
# ... unlimited
```

---

## 📊 API Response

TextBelt returns helpful information:

```json
{
  "success": true,
  "textId": 123456789,
  "quotaRemaining": 0  // For free tier (1 per day per number)
}
```

If quota exceeded:

```json
{
  "success": false,
  "error": "Out of quota",
  "quotaRemaining": 0
}
```

---

## 🎯 Usage Examples

### Example 1: Free Tier Testing

```bash
# Start mobile testing C2 panel
./scripts/start_mobile_testing.sh

# In C2 panel (http://localhost:5007):
# - Enter phone: +15555551234
# - Type message: "Security test"
# - Click Send

# Result: SMS sent immediately (free tier)
# Wait 24 hours before sending to same number again
```

### Example 2: Production Exercise (Paid Tier)

```bash
# Step 1: Purchase API key from https://textbelt.com/purchase
# Step 2: Update .env
TEXTBELT_API_KEY=your_purchased_key_here

# Step 3: Set live mode
DEMO_MODE=false

# Step 4: Start testing
./scripts/start_mobile_testing.sh

# Now you can send unlimited SMS messages!
```

---

## 🔬 Testing Your Setup

### Test 1: Demo Mode (No Real SMS)

```bash
# .env should have:
DEMO_MODE=true

# Start C2 panel
./scripts/start_mobile_testing.sh

# Send test SMS
# Result: Simulated (logged but not actually sent)
```

### Test 2: Live Mode with Free Tier

```bash
# .env should have:
DEMO_MODE=false
TEXTBELT_API_KEY=textbelt

# Start C2 panel
./scripts/start_mobile_testing.sh

# Send test SMS to your own phone
# Result: Real SMS delivered! (1 per day limit)
```

### Test 3: Check Quota

View the C2 panel logs to see quota remaining:

```bash
tail -f logs/mobile_testing.log

# You'll see:
# SMS sent via TextBelt - Quota remaining: 0
```

---

## 💡 Best Practices

### For Testing/Development (Free Tier)

✅ Use different phone numbers for testing
- Test 1: +15555551234 (gets 1 free SMS)
- Test 2: +15555555678 (gets 1 free SMS)
- Test 3: +15555559999 (gets 1 free SMS)

✅ Space out tests across 24 hours

✅ Use demo mode for framework testing

### For Production Red Team Exercises (Paid Tier)

✅ Purchase API key before exercise ($10 = ~1,500 messages)

✅ Test with free tier first to verify setup

✅ Configure authorized targets in `config/mobile_targets.yaml`

✅ Monitor quota in logs

---

## 🛠️ Troubleshooting

### Problem: "Out of quota" error

**Cause**: Free tier limit reached (1 per day per number)

**Solution**:
- Wait 24 hours
- OR use different phone number
- OR purchase API key

### Problem: SMS not delivered

**Check**:
1. Phone number format correct? (+1234567890)
2. Demo mode disabled? (`DEMO_MODE=false`)
3. Check logs: `tail -f logs/mobile_testing.log`
4. Valid phone number? (not VoIP/landline)

### Problem: Want to send more than 1 SMS per day

**Solution**: Purchase API key from https://textbelt.com/purchase

Cost example:
- $10 = ~1,500 SMS messages
- $25 = ~3,900 SMS messages

---

## 📈 Cost Comparison

| Service | Free Tier | Paid Cost | Notes |
|---------|-----------|-----------|-------|
| **TextBelt** | 1 SMS/day/number | $0.0064/msg | No signup, pay-as-you-go |
| Twilio | Trial credits | $0.0075/msg | Requires account, monthly fees |
| AWS SNS | None | $0.00645/msg | Requires AWS account |

**Winner**: TextBelt for simplicity and cost! ✅

---

## 🔐 Security Notes

### API Key Storage

- Store API key in `.env` file (already gitignored)
- Never commit API keys to git
- Rotate keys periodically

### Rate Limiting

TextBelt has built-in rate limiting:
- Free tier: 1 per day per number
- Paid tier: Reasonable limits (no spam)

### Authorized Targets

Always use `config/mobile_targets.yaml` to control who can be targeted!

---

## 🎓 Quick Reference

### Current Configuration

```bash
# Your current setup (in .env):
TEXTBELT_API_KEY=textbelt          # Free tier
DEMO_MODE=true                     # Safe simulation mode
```

### To Enable Real SMS (Free Tier)

```bash
# Change to:
DEMO_MODE=false
TEXTBELT_API_KEY=textbelt          # Keep as is
```

### To Enable Unlimited SMS (Paid)

```bash
# Get API key from textbelt.com/purchase
# Then change to:
DEMO_MODE=false
TEXTBELT_API_KEY=your_purchased_key_here
```

---

## 📞 Support

- **TextBelt Docs**: https://textbelt.com
- **Purchase API Key**: https://textbelt.com/purchase
- **Check Quota**: Monitor C2 panel logs

---

## ✅ Summary

**You're already configured for TextBelt!**

- ✅ Free tier enabled by default
- ✅ No signup required
- ✅ 1 SMS per day per number
- ✅ Perfect for testing

**Ready to send your first SMS?**

```bash
./scripts/start_mobile_testing.sh
# Open: http://localhost:5007
# Send a test SMS!
```

**For production red team exercises:**

1. Purchase API key: https://textbelt.com/purchase
2. Update `.env`: `TEXTBELT_API_KEY=your_key`
3. Set live mode: `DEMO_MODE=false`
4. Send unlimited SMS! 🚀
