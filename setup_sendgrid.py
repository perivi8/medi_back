#!/usr/bin/env python3
"""
SendGrid Setup Helper for MediCare+ Platform
Helps configure SendGrid for email delivery on Render
"""

import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue with system environment

def show_sendgrid_setup_instructions():
    """Show detailed SendGrid setup instructions"""
    print("="*80)
    print("📧 SENDGRID SETUP HELPER - MediCare+ Platform")
    print("="*80)
    print()
    print("🎯 PROBLEM: Emails are being stored locally instead of being sent")
    print("❓ REASON: SendGrid API key is not configured")
    print("✅ SOLUTION: Set up SendGrid for reliable email delivery")
    print()
    
    print("📋 STEP-BY-STEP SETUP INSTRUCTIONS:")
    print("="*50)
    print()
    
    print("1. CREATE SENDGRID ACCOUNT:")
    print("   • Go to https://sendgrid.com")
    print("   • Sign up for free account (100 emails/day)")
    print("   • Verify your email address")
    print()
    
    print("2. CREATE API KEY:")
    print("   • In SendGrid dashboard, go to Settings → API Keys")
    print("   • Click 'Create API Key'")
    print("   • Name it 'MediCare-Render'")
    print("   • Select 'Restricted Access'")
    print("   • Under 'Mail Send', select 'Full Access'")
    print("   • Click 'Create & View'")
    print("   • COPY the API key (you won't see it again)")
    print()
    
    print("3. CONFIGURE RENDER ENVIRONMENT:")
    print("   • Go to your Render dashboard")
    print("   • Select your MediCare+ backend service")
    print("   • Go to 'Environment' tab")
    print("   • Add environment variable:")
    print("     Key: SENDGRID_API_KEY")
    print("     Value: [your copied API key]")
    print()
    
    print("4. VERIFY SENDER IDENTITY:")
    print("   • In SendGrid dashboard, go to Settings → Sender Authentication")
    print("   • Click 'Verify a Single Sender'")
    print("   • Fill in your details:")
    print("     - From Email: perivihk@gmail.com")
    print("     - From Name: MediCare+ Platform")
    print("     - Reply To: perivihk@gmail.com")
    print("   • Click 'Create'")
    print()
    
    print("5. REDeploy YOUR SERVICE:")
    print("   • In Render dashboard, click 'Manual Deploy'")
    print("   • Or push a small change to trigger automatic deployment")
    print()
    
    print("✅ EXPECTED RESULTS AFTER SETUP:")
    print("- Emails will be sent via SendGrid within 5-10 seconds")
    print("- No more 'stored locally' messages")
    print("- Professional emails delivered to inbox")
    print("- Reliable email service on Render")
    print()
    
    print("💡 TIPS:")
    print("- Keep your API key secure and private")
    print("- The free tier allows 100 emails/day")
    print("- Check spam folder if emails don't appear in inbox")
    print("- Monitor SendGrid dashboard for delivery analytics")
    print()
    
    print("="*80)
    print("Need help? Check SENDGRID_SETUP_GUIDE.md for detailed instructions")
    print("="*80)

def check_current_configuration():
    """Check current email configuration"""
    print("🔍 CURRENT EMAIL CONFIGURATION CHECK:")
    print("="*50)
    
    # Check SendGrid API key
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if sendgrid_key:
        print(f"✅ SendGrid API Key: CONFIGURED")
        print(f"   Length: {len(sendgrid_key)} characters")
        if sendgrid_key.startswith('SG.'):
            print("   Format: VALID (starts with SG.)")
        else:
            print("   ⚠️ Format: MAY BE INVALID (should start with SG.)")
    else:
        print("❌ SendGrid API Key: NOT CONFIGURED")
    
    # Check Gmail credentials
    gmail_email = os.environ.get('GMAIL_EMAIL')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if gmail_email and gmail_password:
        print(f"📧 Gmail Email: {gmail_email}")
        print("🔑 Gmail App Password: CONFIGURED")
        print("⚠️  NOTE: Gmail SMTP may not work on Render due to blocked ports")
    elif gmail_email:
        print(f"📧 Gmail Email: {gmail_email}")
        print("❌ Gmail App Password: NOT CONFIGURED")
    else:
        print("📧 Gmail Email: NOT CONFIGURED")
    
    print()
    
    # Check available email providers
    try:
        from render_http_email_service import render_http_email_service
        providers = render_http_email_service.available_providers
        provider_names = [p['name'] for p in providers]
        print(f"🔧 Available Email Providers: {provider_names}")
        
        if 'SendGrid' in provider_names:
            print("✅ SendGrid is available")
        else:
            print("❌ SendGrid is not available (missing API key)")
            
        if 'Local Storage' in provider_names:
            print("⚠️  Using Local Storage as fallback")
            print("   This means emails are being stored locally instead of sent")
    except ImportError:
        print("❌ Could not check email providers - service not available")

def main():
    """Main function"""
    print("🏥 MEDI-CARE+ EMAIL SETUP HELPER")
    print("="*50)
    print()
    
    # Check current configuration
    check_current_configuration()
    print()
    
    # Show setup instructions
    show_sendgrid_setup_instructions()
    
    print()
    print("🔧 QUICK TEST COMMANDS:")
    print("   cd backend && python test_sendgrid_simple.py")
    print("   cd backend && python test_email_functionality_fixed.py")
    print()

if __name__ == "__main__":
    main()