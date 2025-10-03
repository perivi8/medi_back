#!/usr/bin/env python3
"""
Complete SendGrid Fix for MediCare+ Platform
Fixes SendGrid authentication errors and updates all necessary configurations
"""

import os
import sys
import subprocess
import json
from dotenv import load_dotenv, set_key

def check_sendgrid_status():
    """Check current SendGrid status"""
    print("🔍 Checking SendGrid configuration status...")
    
    # Load environment
    load_dotenv()
    
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    
    if not sendgrid_key:
        print("❌ SENDGRID_API_KEY not found in environment")
        return False, "NOT_FOUND"
        
    if sendgrid_key == "SG.your_sendgrid_api_key_here":
        print("❌ Current API key is a placeholder")
        return False, "PLACEHOLDER"
        
    if not sendgrid_key.startswith("SG."):
        print("❌ API key format is invalid")
        return False, "INVALID_FORMAT"
        
    if len(sendgrid_key) < 20:
        print("❌ API key seems too short")
        return False, "TOO_SHORT"
        
    print("✅ SendGrid API key appears to be properly configured")
    return True, "VALID"

def get_valid_sendgrid_key():
    """Get a valid SendGrid API key from user"""
    print("\n" + "="*60)
    print("🔐 GET VALID SENDGRID API KEY")
    print("="*60)
    
    print("\n📋 To fix the SendGrid authentication error, you need a real API key:")
    print("1. Go to https://sendgrid.com")
    print("2. Sign up for a free account (100 emails/day)")
    print("3. Create an API key with Mail Send permissions")
    print("4. Copy the API key")
    
    while True:
        api_key = input("\n📋 Paste your SendGrid API key: ").strip()
        
        if not api_key:
            print("❌ Please enter a valid API key")
            continue
            
        if not api_key.startswith("SG."):
            print("❌ Invalid format - API key must start with 'SG.'")
            continue
            
        if len(api_key) < 20:
            print("❌ API key seems too short - please check")
            continue
            
        return api_key

def update_local_env(api_key):
    """Update local .env file"""
    print("\n🔄 Updating local environment configuration...")
    
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"❌ {env_file} not found")
        return False
        
    try:
        set_key(env_file, "SENDGRID_API_KEY", api_key)
        print("✅ Updated .env file with new SendGrid API key")
        return True
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        return False

def update_render_env(api_key):
    """Update Render environment variables"""
    print("\n🔄 Updating Render environment variables...")
    
    try:
        # This would typically involve Render API calls
        # For now, we'll just provide instructions
        print("📋 To update Render environment variables:")
        print("1. Go to your Render dashboard")
        print("2. Select your MediCare+ backend service")
        print("3. Go to 'Environment' tab")
        print("4. Find 'SENDGRID_API_KEY' variable")
        print("5. Update it with your actual API key")
        print("6. Click 'Save Changes'")
        print("7. Redeploy your service")
        return True
    except Exception as e:
        print(f"❌ Failed to update Render environment: {e}")
        return False

def test_sendgrid_functionality():
    """Test SendGrid functionality"""
    print("\n🧪 Testing SendGrid functionality...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_sendgrid_simple.py"
        ], capture_output=True, text=True, timeout=30)
        
        print("📝 Test output:")
        print(result.stdout)
        
        if "SUCCESS! Email sent via SendGrid" in result.stdout:
            print("✅ SendGrid is working correctly!")
            return True
        elif "Email stored locally" in result.stdout:
            print("❌ SendGrid is still not working - email stored locally")
            return False
        else:
            print("⚠️ Test completed but status unclear")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_troubleshooting_guide():
    """Show troubleshooting guide"""
    print("\n" + "="*60)
    print("🛠️ TROUBLESHOOTING GUIDE")
    print("="*60)
    
    print("\nIf SendGrid is still not working:")
    print("1. Check Render logs for detailed error messages")
    print("2. Verify API key has correct permissions (Mail Send: Full Access)")
    print("3. Ensure sender identity is verified in SendGrid")
    print("4. Check if you've hit the free tier limit (100 emails/day)")
    print("5. Try creating a new API key")
    
    print("\nAlternative email providers:")
    print("1. Mailgun: Sign up at https://www.mailgun.com/")
    print("2. Gmail SMTP: Use with App Password (less reliable on Render)")

def main():
    """Main function"""
    print("🏥 COMPLETE SENDGRID FIX FOR MEDI-CARE+ PLATFORM")
    print("="*60)
    
    # Check current status
    is_valid, status = check_sendgrid_status()
    
    if is_valid:
        print("\n✅ SendGrid appears to be correctly configured!")
        response = input("Do you want to update it anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Keeping current configuration.")
            return
    
    # Get valid API key
    api_key = get_valid_sendgrid_key()
    if not api_key:
        print("❌ Failed to get valid API key")
        return
    
    # Update configurations
    local_success = update_local_env(api_key)
    
    print("\n" + "="*60)
    print("🔧 CONFIGURATION UPDATES")
    print("="*60)
    
    if local_success:
        print("✅ Local .env file updated successfully")
    else:
        print("❌ Failed to update local .env file")
    
    # Show Render update instructions
    update_render_env(api_key)
    
    # Test functionality
    print("\n" + "="*60)
    print("🧪 FUNCTIONALITY TEST")
    print("="*60)
    
    test_result = test_sendgrid_functionality()
    
    if test_result:
        print("\n🎉 SUCCESS! SendGrid authentication error has been fixed!")
        print("📧 Emails should now be sent via SendGrid instead of being stored locally")
    else:
        print("\n❌ SendGrid is still not working properly")
        show_troubleshooting_guide()
    
    print("\n" + "="*60)
    print("📄 DOCUMENTATION")
    print("="*60)
    print("For detailed instructions, see: FIX_SENDGRID_AUTH_ERROR.md")

if __name__ == "__main__":
    main()