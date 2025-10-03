#!/usr/bin/env python3
"""
Test script to verify SendGrid fix
"""

import os
from dotenv import load_dotenv

def test_sendgrid_config():
    """Test SendGrid configuration"""
    print("🔍 Testing SendGrid Configuration")
    print("="*50)
    
    # Load environment variables
    load_dotenv()
    
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    
    if not sendgrid_key:
        print("❌ SENDGRID_API_KEY not found in environment")
        return False
        
    print(f"✅ SENDGRID_API_KEY found: {sendgrid_key[:10]}...")
    
    if sendgrid_key == "SG.your_sendgrid_api_key_here":
        print("❌ Current API key is a placeholder - needs to be replaced")
        print("🔧 Run 'python fix_sendgrid_auth.py' to fix this")
        return False
    
    if not sendgrid_key.startswith("SG."):
        print("❌ API key format is invalid - should start with 'SG.'")
        return False
        
    if len(sendgrid_key) < 20:
        print("❌ API key seems too short - might be invalid")
        return False
        
    print("✅ SendGrid API key appears to be valid")
    print("🎉 SendGrid should work correctly now!")
    return True

if __name__ == "__main__":
    test_sendgrid_config()