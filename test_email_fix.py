#!/usr/bin/env python3
"""
Test the email fix for network issues
"""

import asyncio
import os
from dotenv import load_dotenv
from email_service import EmailService

async def test_email_network_error():
    """Test email sending with network error handling"""
    print("🔍 Testing Email Network Error Handling")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Create email service
    email_service = EmailService()
    
    # Check if email service is enabled
    if not email_service.is_email_enabled():
        print("❌ Email service is not enabled")
        return False
    
    print(f"✅ Email service enabled - Sender: {email_service.sender_email}")
    
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
    if 'network_error' in result:
        print(f"   Network Error: {'YES' if result.get('network_error') else 'NO'}")
    if 'error' in result:
        print(f"   Error Details: {result.get('error')}")
    
    # Check if report was stored locally
    try:
        import json
        if os.path.exists("email_reports.json"):
            with open("email_reports.json", 'r') as f:
                reports = json.load(f)
                if reports:
                    latest_report = reports[-1]
                    if latest_report.get("recipient") == test_email:
                        print("✅ Email report was stored locally as backup")
                    else:
                        print("⚠️ Local storage may have issues")
                else:
                    print("⚠️ No reports found in local storage")
        else:
            print("⚠️ Email reports file not found")
    except Exception as e:
        print(f"⚠️ Could not verify local storage: {e}")
    
    return result.get('success', False)

if __name__ == "__main__":
    asyncio.run(test_email_network_error())