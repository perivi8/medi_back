#!/usr/bin/env python3
"""
Network-aware Email Service Wrapper
Handles network connectivity issues gracefully and provides better fallback mechanisms
"""

import asyncio
import socket
from email_service import EmailService

class NetworkAwareEmailService:
    def __init__(self):
        self.email_service = EmailService()
        self.network_test_host = "smtp.gmail.com"
        self.network_test_port = 587
        self.network_test_timeout = 5
    
    def is_network_available(self):
        """Test if network connectivity to Gmail SMTP is available"""
        try:
            # Test DNS resolution
            socket.gethostbyname(self.network_test_host)
            
            # Test port connectivity
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.network_test_timeout)
            result = sock.connect_ex((self.network_test_host, self.network_test_port))
            sock.close()
            
            return result == 0
        except:
            return False
    
    async def send_prediction_email_async(self, recipient_email: str, prediction_data: dict, patient_data: dict):
        """Send prediction email with network awareness"""
        
        # Check if email service is enabled
        if not self.email_service.is_email_enabled():
            return {
                "success": False,
                "message": "Email service is not configured. Please set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables.",
                "network_check": "skipped",
                "fallback": "local_storage"
            }
        
        # Check network connectivity before attempting to send
        if not self.is_network_available():
            # Store locally and return appropriate message
            await self.email_service._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
            return {
                "success": False,
                "message": "Network connectivity issue detected. Email report has been saved locally and will be sent when network connectivity is restored.",
                "network_check": "failed",
                "fallback": "local_storage"
            }
        
        # Network seems available, try to send email
        try:
            result = await self.email_service.send_prediction_email_async(
                recipient_email=recipient_email,
                prediction_data=prediction_data,
                patient_data=patient_data
            )
            
            # Add network check info to result
            result["network_check"] = "passed"
            return result
            
        except Exception as e:
            # Handle network-specific errors
            error_msg = str(e).lower()
            if "network is unreachable" in error_msg or "errno 101" in error_msg or "timeout" in error_msg:
                # Store locally as fallback
                await self.email_service._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
                return {
                    "success": False,
                    "message": f"Network connectivity issue detected during email sending: {str(e)}. Email report has been saved locally and will be sent when network connectivity is restored.",
                    "network_check": "passed_but_failed_during_send",
                    "error": str(e),
                    "fallback": "local_storage"
                }
            else:
                # Re-raise non-network errors
                raise e

# Global instance
network_aware_email_service = NetworkAwareEmailService()