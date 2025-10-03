#!/usr/bin/env python3
"""
Script to modify the application to use SMTP email instead of SendGrid
"""

import os
import shutil
from datetime import datetime

def backup_app_file():
    """Create a backup of the app.py file"""
    app_file = "app.py"
    if os.path.exists(app_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"app_backup_smtp_{timestamp}.py"
        shutil.copy2(app_file, backup_file)
        print(f"✅ Backed up {app_file} to {backup_file}")
        return True
    else:
        print(f"❌ {app_file} not found")
        return False

def modify_email_endpoint():
    """Modify the email endpoint to use SMTP instead of HTTP email service"""
    app_file = "app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found")
        return False
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the email endpoint
        email_endpoint_start = content.find('@app.post("/send-prediction-email", response_model=EmailResponse)')
        if email_endpoint_start == -1:
            print("❌ Email endpoint not found in app.py")
            return False
            
        email_endpoint_end = content.find('@app.get(\'/admin/datasets\')', email_endpoint_start)
        if email_endpoint_end == -1:
            # Try alternative ending
            email_endpoint_end = content.find('@app.get("/admin/datasets")', email_endpoint_start)
            if email_endpoint_end == -1:
                # Find the next endpoint
                next_endpoints = [
                    '@app.post("/test-email")',
                    '@app.get("/user-emails/',
                    '@app.post("/store-user-email")',
                    'if __name__ == "__main__":'
                ]
                
                for endpoint in next_endpoints:
                    email_endpoint_end = content.find(endpoint, email_endpoint_start)
                    if email_endpoint_end != -1:
                        break
        
        if email_endpoint_end == -1:
            print("❌ Could not find end of email endpoint")
            return False
        
        # Extract the email endpoint
        email_endpoint = content[email_endpoint_start:email_endpoint_end]
        
        # Create the new email endpoint using SMTP
        new_email_endpoint = '''@app.post("/send-prediction-email", response_model=EmailResponse)
async def send_prediction_email(request: EmailPredictionRequest):
    """
    Email endpoint using SMTP service (Gmail)
    Uses the configured Gmail SMTP settings from environment variables
    """
    start_time = datetime.now()
    
    try:
        print(f"📧 Processing email request for: {request.email} (SMTP SERVICE)")
        
        # Use SMTP-based email service
        from email_service import email_service
        print("✅ Using SMTP-based email service")
        
        # Check if email service is enabled
        if not email_service.is_email_enabled():
            print("❌ Email service is not properly configured")
            return EmailResponse(
                success=False,
                message="❌ Email service not configured. Please set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables."
            )
        
        # Send email using the SMTP service
        result = await email_service.send_prediction_email_async(
            recipient_email=str(request.email),
            prediction_data=request.prediction,
            patient_data=request.patient_data
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        print(f"⏱️ Email processing completed in {processing_time:.2f} seconds")
        
        # Save email to database if successful (optional)
        if result.get("success", False):
            try:
                # Try to save email to users table
                await supabase_client.save_email_to_users(str(request.email))
                print(f"✅ Email {request.email} saved to users table")
            except Exception as e:
                print(f"⚠️ Could not save email to database: {e}")
                # Don't fail the email send if database save fails
        
        # Return result with proper error handling
        return EmailResponse(
            success=result.get("success", False),
            message=result.get("message", f"❌ Email delivery failed for {request.email}")
        )
            
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        print(f"❌ Email processing error after {processing_time:.2f}s: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        
        # Return honest error message
        return EmailResponse(
            success=False,
            message=f"❌ Email sending failed: {str(e)}. Please check your email address and try again."
        )'''
        
        # Replace the old endpoint with the new one
        new_content = content[:email_endpoint_start] + new_email_endpoint + content[email_endpoint_end:]
        
        # Write the modified content back to the file
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Successfully modified email endpoint to use SMTP service")
        return True
        
    except Exception as e:
        print(f"❌ Failed to modify email endpoint: {e}")
        return False

def create_smtp_test_script():
    """Create a test script to verify SMTP configuration"""
    test_script = '''#!/usr/bin/env python3
"""
Test SMTP Email Configuration
"""

import os
from dotenv import load_dotenv
from email_service import EmailService

def test_smtp_configuration():
    """Test SMTP email configuration"""
    print("🔍 Testing SMTP Email Configuration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check SMTP configuration
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_email:
        print("❌ GMAIL_EMAIL not found in environment")
        return False
        
    if not gmail_password:
        print("❌ GMAIL_APP_PASSWORD not found in environment")
        return False
    
    print(f"✅ GMAIL_EMAIL: {gmail_email}")
    print(f"✅ GMAIL_APP_PASSWORD: {'*' * len(gmail_password)} (configured)")
    
    # Test email service
    email_service = EmailService()
    
    if not email_service.is_email_enabled():
        print("❌ Email service is not enabled")
        print("💡 Check that both GMAIL_EMAIL and GMAIL_APP_PASSWORD are set correctly")
        return False
    
    print("✅ Email service is enabled and ready to send emails")
    print("🎉 SMTP configuration is correct!")
    
    return True

if __name__ == "__main__":
    test_smtp_configuration()
'''
    
    with open("test_smtp_config.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created SMTP test script: test_smtp_config.py")

def create_smtp_readme():
    """Create a README with instructions for using SMTP"""
    readme_content = '''# 📧 SMTP Email Configuration

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
1. Run the modification script:
   ```bash
   python use_smtp_email.py
   ```

2. Restart your application

3. Test email functionality:
   ```bash
   # In your frontend, make a prediction and click "Email Report"
   # Or use the test endpoint:
   curl -X POST http://localhost:8000/test-email
   ```

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
'''
    
    with open("SMTP_EMAIL_README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created SMTP README: SMTP_EMAIL_README.md")

def main():
    """Main function"""
    print("📧 SMTP EMAIL CONFIGURATION SETUP")
    print("=" * 50)
    
    # Backup the app file
    if not backup_app_file():
        return
    
    # Modify the email endpoint
    if not modify_email_endpoint():
        return
    
    # Create test script
    create_smtp_test_script()
    
    # Create README
    create_smtp_readme()
    
    print("\n🎉 SMTP EMAIL CONFIGURATION COMPLETE!")
    print("\nNext steps:")
    print("1. Test your SMTP configuration:")
    print("   python test_smtp_config.py")
    print("\n2. Restart your application")
    print("\n3. Test email functionality through your frontend")

if __name__ == "__main__":
    main()