#!/usr/bin/env python3
"""
Simple email test
"""

import os
from dotenv import load_dotenv
from fixed_email_service import FixedEmailService

def test_email_service():
    """Test email service initialization"""
    print("🔍 Testing Email Service Initialization")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Create email service
    email_service = FixedEmailService()
    
    print(f"📧 Email enabled: {email_service.is_email_enabled()}")
    print(f"📧 Sender email: {email_service.sender_email}")
    print(f"📧 Password set: {email_service.sender_password is not None}")
    
    return email_service.is_email_enabled()

if __name__ == "__main__":
    test_email_service()
