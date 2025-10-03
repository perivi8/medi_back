#!/usr/bin/env python3
"""
Test SMTP Email Sending
"""

import asyncio
from email_service import email_service

async def test_smtp_email():
    """Test sending an email via SMTP"""
    print("📧 Testing SMTP Email Sending")
    print("=" * 50)
    
    # Check if email service is enabled
    if not email_service.is_email_enabled():
        print("❌ Email service is not enabled")
        return False
    
    print(f"✅ Email service enabled - Sender: {email_service.sender_email}")
    
    # Test data
    test_email = "gowthaamankrishna1998@gmail.com"
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
    
    # Send email
    result = await email_service.send_prediction_email_async(
        recipient_email=test_email,
        prediction_data=test_prediction,
        patient_data=test_patient_data
    )
    
    print(f"📊 Result:")
    print(f"   Success: {'✅ YES' if result.get('success') else '❌ NO'}")
    print(f"   Message: {result.get('message')}")
    if 'send_time' in result:
        print(f"   Send Time: {result.get('send_time')}")
    
    return result.get('success', False)

if __name__ == "__main__":
    asyncio.run(test_smtp_email())