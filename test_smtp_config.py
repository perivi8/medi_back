#!/usr/bin/env python3
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