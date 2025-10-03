#!/usr/bin/env python3
"""
Fix Render Email Service
Automatically configures HTTP-based email service for Render deployment
"""

import os
import sys
from dotenv import load_dotenv

def check_render_environment():
    """Check if we're running on Render"""
    return 'RENDER' in os.environ

def setup_sendgrid_fallback():
    """Setup SendGrid as primary email provider"""
    print("🔧 Setting up SendGrid fallback...")
    
    # Check if SendGrid API key is available
    sendgrid_key = os.getenv('SENDGRID_API_KEY')
    if sendgrid_key:
        print("✅ SendGrid API key found")
        return True
    else:
        print("⚠️ SendGrid API key not found")
        print("💡 Please add SENDGRID_API_KEY to your Render environment variables")
        return False

def verify_email_service():
    """Verify email service is working"""
    print("🔍 Verifying email service...")
    
    try:
        # Try importing the HTTP email service
        from render_http_email_service import render_http_email_service
        service = render_http_email_service
        
        if service.available_providers:
            print("✅ HTTP email service is available")
            print(f"📧 Available providers: {[p['name'] for p in service.available_providers]}")
            return True
        else:
            print("⚠️ No email providers configured")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import HTTP email service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with email service: {e}")
        return False

def create_env_template():
    """Create environment template with SendGrid example"""
    template = '''# Render Environment Variables Template
# Copy these to your Render dashboard Environment Variables

# Required for all deployments
GMAIL_EMAIL=your-gmail@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password

# Recommended for Render (HTTP-based email)
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here

# Alternative email providers
# MAILGUN_API_KEY=your_mailgun_api_key
# MAILGUN_DOMAIN=your_mailgun_domain

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production
'''
    
    with open('render_env_template_with_sendgrid.txt', 'w') as f:
        f.write(template)
    
    print("✅ Created environment template: render_env_template_with_sendgrid.txt")

def main():
    """Main function"""
    print("🚀 Fixing Render Email Service")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if running on Render
    if check_render_environment():
        print("✅ Running on Render platform")
    else:
        print("⚠️ Not running on Render (script designed for Render deployment)")
    
    # Setup SendGrid
    sendgrid_ok = setup_sendgrid_fallback()
    
    # Verify email service
    service_ok = verify_email_service()
    
    # Create environment template
    create_env_template()
    
    print("\n📊 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    if sendgrid_ok and service_ok:
        print("✅ Email service should work properly on Render")
        print("💡 Emails will be sent via SendGrid HTTP API")
    elif service_ok:
        print("✅ Email service available but SendGrid not configured")
        print("💡 Using fallback providers")
    else:
        print("❌ Email service needs configuration")
        print("💡 Please add SendGrid API key to Render environment")
    
    print("\n🔧 NEXT STEPS:")
    print("1. Add SENDGRID_API_KEY to Render environment variables")
    print("2. Verify sender identity in SendGrid dashboard")
    print("3. Redeploy your service")
    print("4. Test email functionality")
    
    return sendgrid_ok and service_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)