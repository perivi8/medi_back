#!/usr/bin/env python3
"""
Test direct Gmail SMTP connection
"""

import smtplib
import ssl
import os
from dotenv import load_dotenv

def test_gmail_connection():
    """Test direct connection to Gmail SMTP"""
    print("🔍 Testing Gmail SMTP Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_email or not gmail_password:
        print("❌ Gmail credentials not found")
        return False
    
    print(f"📧 Testing with email: {gmail_email}")
    
    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    print(f"🔗 Connecting to {smtp_server}:{smtp_port}")
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to server
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            print("🔐 Starting TLS...")
            server.starttls(context=context)
            
            print("🔑 Logging in...")
            server.login(gmail_email, gmail_password)
            
            print("✅ Successfully connected to Gmail SMTP!")
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_gmail_connection()