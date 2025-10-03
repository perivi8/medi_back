#!/usr/bin/env python3
"""
Comprehensive SMTP Email Test
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

def test_environment_variables():
    """Test that environment variables are loaded correctly"""
    print("🔍 Testing Environment Variables")
    print("=" * 50)
    
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    print(f"GMAIL_EMAIL: {gmail_email}")
    print(f"GMAIL_APP_PASSWORD: {'SET' if gmail_password else 'NOT SET'}")
    
    if gmail_email and gmail_password:
        print("✅ Environment variables loaded correctly")
        return True
    else:
        print("❌ Environment variables not loaded correctly")
        return False

def test_email_service():
    """Test the email service"""
    print("\n📧 Testing Email Service")
    print("=" * 50)
    
    try:
        from email_service import EmailService
        email_service = EmailService()
        
        print(f"Email enabled: {email_service.is_email_enabled()}")
        print(f"Sender email: {email_service.sender_email}")
        print(f"Sender password set: {bool(email_service.sender_password)}")
        
        if email_service.is_email_enabled():
            print("✅ Email service is properly configured")
            return True
        else:
            print("❌ Email service is not properly configured")
            return False
    except Exception as e:
        print(f"❌ Error testing email service: {e}")
        return False

def test_smtp_connection():
    """Test SMTP connection"""
    print("\n🔗 Testing SMTP Connection")
    print("=" * 50)
    
    try:
        from email_service import EmailService
        email_service = EmailService()
        
        if not email_service.is_email_enabled() or not email_service.sender_email or not email_service.sender_password:
            print("❌ Email service not enabled or credentials missing, cannot test connection")
            return False
        
        import smtplib
        import ssl
        
        print(f"Connecting to {email_service.smtp_server}:{email_service.smtp_port}")
        
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Connect to server
        with smtplib.SMTP(email_service.smtp_server, email_service.smtp_port, timeout=10) as server:
            print("✅ Connected to SMTP server")
            server.starttls(context=context)
            print("✅ TLS started")
            server.login(email_service.sender_email, email_service.sender_password)
            print("✅ Login successful")
            
        print("🎉 SMTP connection test passed!")
        return True
        
    except Exception as e:
        print(f"❌ SMTP connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("🏥 COMPREHENSIVE SMTP EMAIL TEST")
    print("=" * 50)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    # Test email service
    service_ok = test_email_service()
    
    # Test SMTP connection
    smtp_ok = False
    if service_ok:
        smtp_ok = test_smtp_connection()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Email Service: {'✅ PASS' if service_ok else '❌ FAIL'}")
    print(f"SMTP Connection: {'✅ PASS' if smtp_ok else '❌ FAIL'}")
    
    if env_ok and service_ok and smtp_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your SMTP email configuration is working correctly.")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("Please check the output above for details.")

if __name__ == "__main__":
    main()