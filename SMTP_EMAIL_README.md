# 📧 SMTP Email Configuration

## 🎯 Purpose
This configuration uses Gmail SMTP to send emails instead of SendGrid HTTP API.

## ✅ Current Configuration
Your [.env](file:///c%3A/Users/Admin/Desktop/MEDI/india-medical-insurance-backend/.env) file already contains:
```
GMAIL_EMAIL=perivihk@gmail.com
GMAIL_APP_PASSWORD=hgubjyxtimzmneht
```

## 🚀 How It Works
1. The application uses the SMTP settings from your [.env](file:///c%3A/Users/Admin/Desktop/MEDI/india-medical-insurance-backend/.env) file
2. Emails are sent directly via Gmail's SMTP server (smtp.gmail.com:587)
3. No third-party services like SendGrid are needed

## 🧪 Testing SMTP Configuration
Run the test script to verify your SMTP configuration:
```bash
cd india-medical-insurance-backend
python test_smtp_config.py
```

## 🛠️ How to Use
1. The email endpoint in [app.py](file:///c%3A/Users/Admin/Desktop/MEDI/india-medical-insurance-backend/app.py) has been modified to use SMTP
2. Restart your application
3. Test email functionality through your frontend

## 📋 Benefits
- ✅ No need for SendGrid API key
- ✅ Uses your existing Gmail configuration
- ✅ Direct SMTP connection
- ✅ No third-party dependencies for email

## ⚠️ Important Notes
1. Gmail SMTP may not work on Render due to blocked ports (25, 465, 587)
2. If deploying to Render, you might need to use SendGrid or another HTTP-based email service
3. For local development, SMTP should work fine

## 🔧 Troubleshooting
If emails are not sending:
1. Verify your Gmail App Password is correct
2. Check that 2-Factor Authentication is enabled on your Gmail account
3. Ensure your App Password has the correct permissions
4. Check firewall settings if running locally

---
**This configuration uses your existing Gmail SMTP settings instead of SendGrid.**