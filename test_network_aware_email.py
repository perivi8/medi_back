#!/usr/bin/env python3
"""
Test the network-aware email service
"""

import asyncio
import os
from dotenv import load_dotenv
from network_aware_email_service import network_aware_email_service

async def test_network_aware_email():
    """Test network-aware email sending"""
    print("🔍 Testing Network-Aware Email Service")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check network availability
    network_available = network_aware_email_service.is_network_available()
    print(f"🌐 Network connectivity test: {'✅ PASSED' if network_available else '❌ FAILED'}")
    
    # Check if email service is enabled
    email_enabled = network_aware_email_service.email_service.is_email_enabled()
    print(f"📧 Email service enabled: {'✅ YES' if email_enabled else '❌ NO'}")
    
    if not email_enabled:
        print("❌ Email service is not properly configured")
        return False
    
    # Test data
    test_email = "perivihari8@gmail.com"
    test_prediction = {
        "prediction": 25000,
        "confidence": 0.88
    }
    test_patient_data = {
        "age": 28,
        "bmi": 24.5,
        "gender": "Male",
        "smoker": "No",
        "region": "South",
        "premium_annual_inr": 22000
    }
    
    print(f"📤 Sending test email to: {test_email}")
    
    # Send email using network-aware service
    result = await network_aware_email_service.send_prediction_email_async(
        recipient_email=test_email,
        prediction_data=test_prediction,
        patient_data=test_patient_data
    )
    
    print(f"📊 Result:")
    print(f"   Success: {'✅ YES' if result.get('success') else '❌ NO'}")
    print(f"   Message: {result.get('message')}")
    print(f"   Network Check: {result.get('network_check', 'N/A')}")
    if 'send_time' in result:
        print(f"   Send Time: {result.get('send_time')}")
    if 'error' in result:
        print(f"   Error Details: {result.get('error')}")
    print(f"   Fallback Used: {result.get('fallback', 'None')}")
    
    return result.get('success', False)

if __name__ == "__main__":
    asyncio.run(test_network_aware_email())