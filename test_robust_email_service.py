#!/usr/bin/env python3
"""
Test script for the robust email service
"""

import asyncio
import json
from robust_email_service import robust_email_service

async def test_robust_email_service():
    """Test the robust email service with network awareness"""
    
    print("="*60)
    print("TESTING ROBUST EMAIL SERVICE")
    print("="*60)
    
    # Test data
    test_email = "perivihari8@gmail.com"
    test_prediction = {
        "prediction": 35000,
        "confidence": 0.92
    }
    test_patient_data = {
        "age": 35,
        "bmi": 28.5,
        "gender": "Male",
        "smoker": "Yes",
        "region": "South",
        "premium_annual_inr": 25000
    }
    
    print(f"📧 Testing email send to: {test_email}")
    print(f"📊 Prediction: ₹{test_prediction['prediction']:,} (Confidence: {test_prediction['confidence']*100}%)")
    print(f"👤 Patient: {test_patient_data['age']} years old, BMI {test_patient_data['bmi']}")
    
    # Test the robust email service
    try:
        result = await robust_email_service.send_prediction_email_async(
            recipient_email=test_email,
            prediction_data=test_prediction,
            patient_data=test_patient_data
        )
        
        print("\n" + "="*60)
        print("EMAIL SERVICE TEST RESULT")
        print("="*60)
        print(f"✅ Success: {result.get('success', False)}")
        print(f"💬 Message: {result.get('message', 'No message')}")
        
        if 'send_time' in result:
            print(f"⏱️ Send Time: {result['send_time']}")
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        if 'network_error' in result:
            print(f"🌐 Network Error: {result['network_error']}")
        
        # Check if report was stored locally
        try:
            with open("email_reports.json", "r") as f:
                reports = json.load(f)
                if reports:
                    latest_report = reports[-1]
                    print(f"💾 Local Storage: Email report stored for {latest_report['recipient']}")
        except FileNotFoundError:
            print("💾 Local Storage: No local reports file found")
        except Exception as e:
            print(f"💾 Local Storage: Error checking reports - {e}")
            
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_robust_email_service())