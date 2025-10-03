#!/usr/bin/env python3
"""
Fix SendGrid Authentication Error Script
Automatically guides user through fixing SendGrid API key issues
"""

import os
import sys
import re
from dotenv import load_dotenv, set_key

def check_current_sendgrid_config():
    """Check current SendGrid configuration"""
    print("🔍 Checking current SendGrid configuration...")
    
    # Load environment variables
    load_dotenv()
    
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    
    if not sendgrid_key:
        print("❌ SENDGRID_API_KEY not found in environment")
        return False
        
    print(f"✅ SendGrid API Key found: {sendgrid_key[:10]}...{sendgrid_key[-5:]}")
    
    # Check if it's a placeholder
    if sendgrid_key == "SG.your_sendgrid_api_key_here":
        print("❌ Current API key is a placeholder - needs to be replaced")
        return False
    
    # Check format
    if not sendgrid_key.startswith("SG."):
        print("❌ API key format is invalid - should start with 'SG.'")
        return False
        
    if len(sendgrid_key) < 20:
        print("❌ API key seems too short - might be invalid")
        return False
        
    print("✅ SendGrid API key appears to be properly formatted")
    return True

def guide_user_to_get_api_key():
    """Guide user through getting a real SendGrid API key"""
    print("\n" + "="*60)
    print("🔐 SENDGRID API KEY SETUP GUIDE")
    print("="*60)
    
    print("\n📋 STEP 1: Create SendGrid Account")
    print("1. Go to https://sendgrid.com")
    print("2. Sign up for a free account (100 emails/day)")
    print("3. Verify your email address")
    
    print("\n📋 STEP 2: Create API Key")
    print("1. In SendGrid dashboard, go to Settings → API Keys")
    print("2. Click 'Create API Key'")
    print("3. Name it 'MediCare-Platform'")
    print("4. Select 'Restricted Access'")
    print("5. Under 'Mail Send', select 'Full Access'")
    print("6. Click 'Create & View'")
    print("7. COPY the API key (you won't see it again)")
    
    print("\n📋 STEP 3: Enter Your API Key")
    api_key = input("\n Paste your SendGrid API key here: ").strip()
    
    # Validate API key format
    if not api_key.startswith("SG."):
        print("❌ Invalid API key format - must start with 'SG.'")
        return None
        
    if len(api_key) < 20:
        print("❌ API key seems too short - please check and try again")
        return None
        
    return api_key

def update_env_file(api_key):
    """Update the .env file with the new API key"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"❌ {env_file} file not found")
        return False
        
    try:
        # Update using dotenv
        set_key(env_file, "SENDGRID_API_KEY", api_key)
        print(f"✅ Updated {env_file} with new SendGrid API key")
        return True
    except Exception as e:
        print(f"❌ Failed to update {env_file}: {e}")
        return False

def show_verification_instructions():
    """Show instructions for verifying the fix"""
    print("\n" + "="*60)
    print("✅ NEXT STEPS TO VERIFY THE FIX")
    print("="*60)
    
    print("\n🔧 STEP 1: Test SendGrid functionality")
    print("Run this command to test:")
    print("   python test_sendgrid_simple.py")
    
    print("\n🔧 STEP 2: Check for success message")
    print("Look for: '🎉 SUCCESS! Email sent via SendGrid'")
    
    print("\n🔧 STEP 3: If deploying to Render")
    print("1. Add the API key to Render environment variables:")
    print("   Key: SENDGRID_API_KEY")
    print("   Value: [your actual API key]")
    print("2. Redeploy your service")
    
    print("\n🔧 STEP 4: Verify sender identity (optional but recommended)")
    print("1. In SendGrid dashboard, go to Settings → Sender Authentication")
    print("2. Click 'Verify a Single Sender'")
    print("3. Use: perivihk@gmail.com as the sender email")

def main():
    """Main function"""
    print("🏥 MEDI-CARE+ SENDGRID AUTHENTICATION FIX")
    print("="*60)
    
    # Check current configuration
    is_valid = check_current_sendgrid_config()
    
    if is_valid:
        print("\n✅ SendGrid configuration appears to be correct!")
        print("If you're still having issues, the API key might have been revoked.")
        response = input("Do you want to update it anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Keeping current configuration.")
            return
    
    # Guide user to get API key
    api_key = guide_user_to_get_api_key()
    if not api_key:
        print("❌ Failed to get valid API key")
        return
    
    # Update .env file
    if update_env_file(api_key):
        print("\n🎉 SUCCESS! SendGrid API key has been updated")
        show_verification_instructions()
    else:
        print("\n❌ Failed to update API key in .env file")
        print("You'll need to manually update the .env file with your API key")

if __name__ == "__main__":
    main()