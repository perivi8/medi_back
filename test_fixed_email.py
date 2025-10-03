#!/usr/bin/env python3
"""
Test the fixed email service
"""

import asyncio
import os
from dotenv import load_dotenv
from fixed_email_service import fixed_email_service

async def test_fixed_email():
    """Test fixed email sending"""
    print("🔍 Testing Fixed Email Service")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if email service is enabled
    email_enabled = fixed_email_service.is_email_enabled()
    print(f"📧 Email service enabled: {'✅ YES' if email_enabled else '❌ NO'}")
    
    if not email_enabled:
        print("❌ Email service is not properly configured")
        return False
    
    print(f"📧 Sender: {fixed_email_service.sender_email}")
    
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
    
    # Send email using fixed service
    result = await fixed_email_service.send_prediction_email_async(
        recipient_email=test_email,
        prediction_data=test_prediction,
        patient_data=test_patient_data
    )
    
    print(f"📊 Result:")
    print(f"   Success: {'✅ YES' if result.get('success') else '❌ NO'}")
    print(f"   Message: {result.get('message')}")
    if 'send_time' in result:
        print(f"   Send Time: {result.get('send_time')}")
    if 'error' in result:
        print(f"   Error Details: {result.get('error')}")
    if 'network_error' in result:
        print(f"   Network Error: {'YES' if result.get('network_error') else 'NO'}")
    
    return result.get('success', False)

if __name__ == "__main__":
    asyncio.run(test_fixed_email())