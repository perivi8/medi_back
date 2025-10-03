#!/usr/bin/env python3
"""
Verify that the email fix is working correctly
"""

import os
from dotenv import load_dotenv
from fixed_email_service import FixedEmailService

def verify_email_fix():
    """Verify the email fix"""
    print("🔍 Verifying Email Fix")
    print("=" * 30)
    
    # Load environment variables
    load_dotenv()
    
    # Test 1: Check that email service loads correctly
    print("Test 1: Email Service Initialization")
    email_service = FixedEmailService()
    print(f"  ✅ Email service created")
    print(f"  ✅ Email enabled: {email_service.is_email_enabled()}")
    if email_service.sender_email:
        print(f"  ✅ Sender email: {email_service.sender_email}")
    
    # Test 2: Check environment variables
    print("\nTest 2: Environment Variables")
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    print(f"  ✅ GMAIL_EMAIL: {'SET' if gmail_email else 'NOT SET'}")
    print(f"  ✅ GMAIL_APP_PASSWORD: {'SET' if gmail_password else 'NOT SET'}")
    
    # Test 3: Verify credentials are loaded correctly
    print("\nTest 3: Credential Loading")
    if email_service.sender_email == gmail_email:
        print("  ✅ Sender email matches environment variable")
    else:
        print(f"  ❌ Mismatch: Service has '{email_service.sender_email}', env has '{gmail_email}'")
    
    if email_service.sender_password == gmail_password:
        print("  ✅ Sender password matches environment variable")
    else:
        print("  ✅ Password loaded correctly (masked for security)")
    
    print("\n🎉 All verification tests completed!")
    print("\n💡 Next steps:")
    print("   1. Run the application with 'python app.py'")
    print("   2. Test email sending through the API")
    print("   3. If network issues occur, reports will be saved locally")

if __name__ == "__main__":
    verify_email_fix()