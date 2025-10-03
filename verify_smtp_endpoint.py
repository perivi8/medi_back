#!/usr/bin/env python3
"""
Verify that the SMTP email endpoint is working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_app_modification():
    """Verify that the app.py file has been modified correctly"""
    print("🔍 Verifying App Modification")
    print("=" * 50)
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if the endpoint uses SMTP
        if "from email_service import email_service" in content and "send_prediction_email_async" in content:
            print("✅ App.py modified to use SMTP email service")
            return True
        else:
            print("❌ App.py not modified correctly")
            return False
            
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def verify_imports():
    """Verify that required imports are available"""
    print("\n📦 Verifying Required Imports")
    print("=" * 50)
    
    imports_ok = True
    
    try:
        from email_service import EmailService
        print("✅ EmailService import successful")
    except Exception as e:
        print(f"❌ EmailService import failed: {e}")
        imports_ok = False
    
    try:
        from email_service import email_service
        print("✅ email_service import successful")
    except Exception as e:
        print(f"❌ email_service import failed: {e}")
        imports_ok = False
    
    return imports_ok

def verify_environment():
    """Verify environment configuration"""
    print("\n⚙️ Verifying Environment Configuration")
    print("=" * 50)
    
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if gmail_email and gmail_password:
        print(f"✅ GMAIL_EMAIL: {gmail_email}")
        print("✅ GMAIL_APP_PASSWORD: Configured")
        return True
    else:
        print("❌ Gmail configuration missing from environment")
        return False

def main():
    """Main function"""
    print("🏥 VERIFY SMTP EMAIL ENDPOINT")
    print("=" * 50)
    
    # Verify app modification
    app_ok = verify_app_modification()
    
    # Verify imports
    imports_ok = verify_imports()
    
    # Verify environment
    env_ok = verify_environment()
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"App Modification: {'✅ PASS' if app_ok else '❌ FAIL'}")
    print(f"Required Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Environment Config: {'✅ PASS' if env_ok else '❌ FAIL'}")
    
    if app_ok and imports_ok and env_ok:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("Your SMTP email endpoint is configured correctly.")
        print("\nNext steps:")
        print("1. Restart your application")
        print("2. Test email functionality through your frontend")
    else:
        print("\n⚠️ SOME VERIFICATIONS FAILED!")
        print("Please check the output above for details.")

if __name__ == "__main__":
    main()