#!/usr/bin/env python3
"""
Test for network issues with Gmail SMTP
"""

import smtplib
import ssl
import socket
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_network_issue():
    """Test for network issues with Gmail SMTP"""
    print("🔍 Testing Network Issues with Gmail SMTP")
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
    
    # Test DNS resolution
    print("🌐 Testing DNS resolution...")
    try:
        smtp_ip = socket.gethostbyname("smtp.gmail.com")
        print(f"✅ smtp.gmail.com resolves to: {smtp_ip}")
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return False
    
    # Test port connectivity
    print("🔌 Testing port connectivity...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((smtp_ip, 587))
        sock.close()
        
        if result == 0:
            print("✅ Port 587 is accessible")
        else:
            print(f"❌ Port 587 is not accessible (error code: {result})")
            return False
    except Exception as e:
        print(f"❌ Port connectivity test failed: {e}")
        return False
    
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
            
            print("📧 Creating test email...")
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = gmail_email
            msg['To'] = "perivihari8@gmail.com"
            msg['Subject'] = "Test Email - Network Issue Debugging"
            
            body = "This is a test email to debug network issues."
            msg.attach(MIMEText(body, 'plain'))
            
            print("📤 Sending test email...")
            server.sendmail(gmail_email, "perivihari8@gmail.com", msg.as_string())
            
            print("✅ Successfully sent test email!")
            return True
            
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        # Check if it's a network error
        if "Network is unreachable" in str(e):
            print("📡 This is a network connectivity issue")
            print("💡 Possible causes:")
            print("   - Firewall blocking outbound connections")
            print("   - Network restrictions in your environment")
            print("   - ISP blocking SMTP ports")
        return False

if __name__ == "__main__":
    test_network_issue()