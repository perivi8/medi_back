#!/usr/bin/env python3
"""
Script to simulate network failure and test fallback mechanisms
"""

import asyncio
import socket
from robust_email_service import robust_email_service

# Monkey patch socket to simulate network failure
original_gethostbyname = socket.gethostbyname
original_socket_connect = socket.socket.connect

def failing_gethostbyname(hostname):
    """Simulate DNS failure"""
    raise socket.gaierror("Network is unreachable")

def failing_socket_connect(self, address):
    """Simulate connection failure"""
    raise OSError(101, "Network is unreachable")

async def test_network_failure_handling():
    """Test how the robust email service handles network failures"""
    
    print("="*60)
    print("SIMULATING NETWORK FAILURE")
    print("="*60)
    
    # Apply monkey patches to simulate network failure
    socket.gethostbyname = failing_gethostbyname
    socket.socket.connect = failing_socket_connect
    
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
    print("🌐 Network failure simulation active")
    
    try:
        # Test the robust email service with simulated network failure
        result = await robust_email_service.send_prediction_email_async(
            recipient_email=test_email,
            prediction_data=test_prediction,
            patient_data=test_patient_data
        )
        
        print("\n" + "="*60)
        print("NETWORK FAILURE TEST RESULT")
        print("="*60)
        print(f"✅ Success: {result.get('success', False)}")
        print(f"💬 Message: {result.get('message', 'No message')}")
        
        if 'network_error' in result:
            print(f"🌐 Network Error Detected: {result['network_error']}")
        if 'fallback' in result:
            print(f"🔄 Fallback Used: {result['fallback']}")
            
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore original functions
        socket.gethostbyname = original_gethostbyname
        socket.socket.connect = original_socket_connect

if __name__ == "__main__":
    asyncio.run(test_network_failure_handling())