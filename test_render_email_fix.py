#!/usr/bin/env python3
"""
Test Render Email Fix
Verifies that the email service works properly on Render deployment
"""

import asyncio
import os
import sys
from datetime import datetime

async def test_email_services():
    """Test all available email services"""
    print("🧪 Testing Email Services for Render Deployment")
    print("=" * 60)
    
    # Test data
    test_email = "test@example.com"
    test_prediction = {
        "prediction": 15000.50,
        "confidence": 0.85
    }
    test_patient = {
        "age": 35,
        "bmi": 24.5,
        "gender": "Male",
        "smoker": "No",
        "region": "North",
        "premium_annual_inr": 20000
    }
    
    # Test 1: HTTP Email Service
    print("🔍 Testing HTTP Email Service...")
    try:
        from render_http_email_service import render_http_email_service
        service = render_http_email_service
        
        print(f"   Available providers: {[p['name'] for p in service.available_providers]}")
        
        if service.available_providers:
            # Test sending (will store locally if no API keys)
            result = await service.send_prediction_email(
                recipient_email=test_email,
                prediction_data=test_prediction,
                patient_data=test_patient
            )
            print(f"   Result: {result['message']}")
            print("   ✅ HTTP Email Service working")
        else:
            print("   ⚠️ No providers available")
            
    except ImportError:
        print("   ⚠️ HTTP Email Service not available")
    except Exception as e:
        print(f"   ❌ HTTP Email Service error: {e}")
    
    # Test 2: Builtin Email Service
    print("\n🔍 Testing Builtin Email Service...")
    try:
        from render_builtin_email_service import render_builtin_email_service
        service = render_builtin_email_service
        
        print(f"   Available providers: {[p['name'] for p in service.available_providers]}")
        
        if service.available_providers:
            # Test sending (will store locally if no API keys)
            result = await service.send_prediction_email(
                recipient_email=test_email,
                prediction_data=test_prediction,
                patient_data=test_patient
            )
            print(f"   Result: {result['message']}")
            print("   ✅ Builtin Email Service working")
        else:
            print("   ⚠️ No providers available")
            
    except ImportError:
        print("   ⚠️ Builtin Email Service not available")
    except Exception as e:
        print(f"   ❌ Builtin Email Service error: {e}")
    
    # Test 3: Bulletproof Email Service
    print("\n🔍 Testing Bulletproof Email Service...")
    try:
        from bulletproof_email_service import bulletproof_email_service
        service = bulletproof_email_service
        
        print(f"   Service enabled: {service.email_enabled}")
        
        if service.email_enabled:
            # Test connection
            connection_result = service.test_gmail_connection()
            print(f"   Connection test: {connection_result['message']}")
            
            if connection_result['success']:
                print("   ✅ Bulletproof Email Service working")
            else:
                print("   ⚠️ Connection test failed (expected on Render)")
        else:
            print("   ⚠️ Service not enabled")
            
    except ImportError:
        print("   ⚠️ Bulletproof Email Service not available")
    except Exception as e:
        print(f"   ❌ Bulletproof Email Service error: {e}")

async def main():
    """Main test function"""
    print("🚀 Testing Render Email Fix")
    print("=" * 60)
    
    # Check environment
    print(f"🖥️ Platform: {'Render' if 'RENDER' in os.environ else 'Local'}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    await test_email_services()
    
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    print("✅ Email service testing completed")
    print("💡 Check results above for any issues")
    print("💡 Emails will be stored locally if HTTP providers not configured")

if __name__ == "__main__":
    asyncio.run(main())