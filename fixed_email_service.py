#!/usr/bin/env python3
"""
Fixed Email Service for MediCare+ Platform
Handles network connectivity issues gracefully
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import asyncio
from datetime import datetime
from jinja2 import Template
import json
from typing import Dict, Any
import concurrent.futures
import socket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FixedEmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_EMAIL")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")
        self.sender_name = "MediCare+ Platform"
        self.email_enabled = bool(self.sender_email and self.sender_password)
        
        # Timeout settings optimized for Render
        self.connection_timeout = 15  # 15 seconds for connection
        self.send_timeout = 30        # 30 seconds for sending
        self.total_timeout = 45       # 45 seconds total (well under 90s frontend timeout)
        
        if not self.email_enabled:
            print("⚠️ Email service disabled - Gmail credentials not configured")
            print("💡 Set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables to enable email")
        else:
            print(f"✅ Email service enabled - Sender: {self.sender_email}")
            print(f"⏱️ Timeout settings: Connection={self.connection_timeout}s, Send={self.send_timeout}s, Total={self.total_timeout}s")
    
    def is_email_enabled(self) -> bool:
        """Check if email service is properly configured"""
        return self.email_enabled and self.sender_email is not None and self.sender_password is not None
        
    def create_prediction_email_template(self) -> str:
        """Create HTML email template for prediction reports"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare+ Prediction Report</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f4f4f4; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 24px; }
        .header p { margin: 5px 0 0 0; opacity: 0.9; }
        .section { margin-bottom: 25px; }
        .section h2 { color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 5px; margin-bottom: 15px; }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .info-item { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #667eea; }
        .info-item strong { color: #333; display: block; margin-bottom: 5px; }
        .prediction-highlight { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }
        .prediction-highlight .amount { font-size: 28px; font-weight: bold; margin-bottom: 5px; }
        .prediction-highlight .confidence { opacity: 0.9; }
        .risk-assessment { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .risk-high { background: #f8d7da; border-color: #f5c6cb; }
        .risk-low { background: #d4edda; border-color: #c3e6cb; }
        .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px; }
        .disclaimer { background: #e9ecef; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 12px; color: #666; }
        @media (max-width: 600px) { .info-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 MediCare+ Medical Insurance Report</h1>
            <p>Professional AI-Powered Insurance Claim Analysis</p>
            <p style="font-size: 12px; opacity: 0.8;">This is an official report from MediCare+ Platform</p>
        </div>
        
        <div class="section">
            <h2>📋 Patient Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Age</strong>
                    {{ patient_data.age }} years
                </div>
                <div class="info-item">
                    <strong>BMI</strong>
                    {{ patient_data.bmi }}
                </div>
                <div class="info-item">
                    <strong>Gender</strong>
                    {{ patient_data.gender }}
                </div>
                <div class="info-item">
                    <strong>Smoking Status</strong>
                    {{ patient_data.smoker }}
                </div>
                <div class="info-item">
                    <strong>Region</strong>
                    {{ patient_data.region }}
                </div>
                <div class="info-item">
                    <strong>Annual Premium</strong>
                    ₹{{ patient_data.premium_annual_inr or 'Estimated' }}
                </div>
            </div>
        </div>
        
        <div class="prediction-highlight">
            <div class="amount">{{ prediction_amount }}</div>
            <div class="confidence">Confidence: {{ confidence }}% | Generated: {{ timestamp }}</div>
        </div>
        
        <div class="section">
            <h2>🎯 BMI Analysis</h2>
            <div class="info-item">
                <strong>BMI Category</strong>
                {{ bmi_category }}
            </div>
            <div class="risk-assessment {{ risk_class }}">
                <strong>Health Risk Level: {{ risk_level }}</strong>
                <p>{{ risk_description }}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Key Insights</h2>
            <ul>
                {% for insight in insights %}
                <li>{{ insight }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong> This AI-generated prediction is for educational and informational purposes only. 
            It should not be used as a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult with qualified healthcare providers for medical decisions.
        </div>
        
        <div class="footer">
            <p><strong>MediCare+ AI Platform</strong> | © 2024 MediCare+ Healthcare Technology</p>
            <p>Powered by Advanced Machine Learning & Medical Data Analytics</p>
            <p>Report generated on {{ timestamp }} for {{ recipient_email }}</p>
            <p style="margin-top: 10px; font-size: 10px; color: #999;">
                If you received this email by mistake, please contact us at {{ sender_email }}<br>
                This email was sent from an automated system. Please do not reply directly to this email.
            </p>
        </div>
    </div>
</body>
</html>
        """
    
    def format_currency(self, value: float) -> str:
        """Format currency in Indian Rupees"""
        return f"₹{value:,.0f}"
    
    def generate_insights(self, patient_data: Dict, prediction: Dict) -> list:
        """Generate key insights based on patient data and prediction"""
        insights = []
        
        age = int(patient_data.get('age', 0))
        bmi = float(patient_data.get('bmi', 0))
        smoker = patient_data.get('smoker', '')
        
        if age > 50:
            insights.append(f"Age factor: At {age} years, age-related health risks may contribute to higher claim probability")
        
        if bmi < 18.5:
            insights.append("BMI indicates underweight status - consider nutritional consultation")
        elif bmi > 30:
            insights.append("BMI indicates obesity - lifestyle modifications recommended to reduce health risks")
        elif 18.5 <= bmi <= 25:
            insights.append("BMI is in healthy range - maintain current lifestyle for optimal health")
        
        if smoker == 'Yes':
            insights.append("Smoking significantly increases health risks and claim probability - cessation programs recommended")
        else:
            insights.append("Non-smoking status contributes positively to health profile")
        
        confidence = prediction.get('confidence', 0)
        if confidence > 0.8:
            insights.append("High prediction confidence indicates reliable estimate based on comprehensive data analysis")
        elif confidence < 0.6:
            insights.append("Moderate prediction confidence - additional health data may improve accuracy")
        
        return insights
    
    async def send_prediction_email_async(self, recipient_email: str, prediction_data: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async email sending with timeout control for Render deployment"""
        
        # Initialize timeout variable
        original_timeout = None
        
        try:
            # Set socket timeout for the entire operation
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(self.total_timeout)
            
            print(f"📧 Starting async email send to {recipient_email} (timeout: {self.total_timeout}s)")
            
            # Check if email service is enabled
            if not self.is_email_enabled():
                print("⚠️ Email service is disabled - storing locally")
                success = await self._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
                return {
                    "success": False,
                    "message": f"Email service is not configured. Gmail credentials (GMAIL_EMAIL and GMAIL_APP_PASSWORD) are required to send emails.",
                    "mock": True,
                    "demo_mode": True
                }
            
            # Prepare email data quickly
            prediction_amount = self.format_currency(prediction_data.get('prediction', 0))
            confidence = round(prediction_data.get('confidence', 0) * 100, 1)
            timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p IST")
            
            # BMI analysis (simplified for speed)
            bmi = float(patient_data.get('bmi', 0))
            if bmi < 18.5:
                bmi_category, risk_level, risk_class = "Underweight", "Moderate", "risk-assessment"
                risk_description = "BMI below normal range may indicate nutritional deficiencies"
            elif bmi < 25:
                bmi_category, risk_level, risk_class = "Normal Weight", "Low", "risk-low"
                risk_description = "BMI in healthy range - optimal for insurance risk assessment"
            elif bmi < 30:
                bmi_category, risk_level, risk_class = "Overweight", "Moderate", "risk-assessment"
                risk_description = "BMI above normal range - lifestyle modifications recommended"
            else:
                bmi_category, risk_level, risk_class = "Obese", "High", "risk-high"
                risk_description = "BMI indicates obesity - significant health risks and higher claim probability"
            
            # Generate insights quickly
            insights = self.generate_insights(patient_data, prediction_data)
            
            # Create lightweight email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🏥 MediCare+ Report - {prediction_amount}"
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['X-Mailer'] = "MediCare+ v1.0"
            
            # Create HTML content
            template = Template(self.create_prediction_email_template())
            html_content = template.render(
                patient_data=patient_data,
                prediction_amount=prediction_amount,
                confidence=confidence,
                timestamp=timestamp,
                bmi_category=bmi_category,
                risk_level=risk_level,
                risk_class=risk_class,
                risk_description=risk_description,
                insights=insights,
                recipient_email=recipient_email,
                sender_email=self.sender_email
            )
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email with strict timeout control
            print(f"🔗 Connecting to {self.smtp_server}:{self.smtp_port} (timeout: {self.connection_timeout}s)")
            
            # Use executor for timeout control
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self._send_email_sync_optimized, msg, recipient_email)
                try:
                    result = await asyncio.wait_for(
                        loop.run_in_executor(None, lambda: future.result()), 
                        timeout=self.total_timeout
                    )
                    
                    print(f"✅ Email sent successfully to {recipient_email}")
                    return {
                        "success": True,
                        "message": f"Prediction report sent successfully to {recipient_email}! Check your inbox.",
                        "send_time": result.get("send_time", "unknown")
                    }
                    
                except asyncio.TimeoutError:
                    print(f"⏱️ Email send timeout after {self.total_timeout}s - storing locally")
                    future.cancel()
                    success = await self._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
                    return {
                        "success": False,
                        "message": f"Email sending timed out after {self.total_timeout} seconds. Please try again or check your internet connection.",
                        "timeout": True
                    }
                except Exception as e:
                    print(f"⚠️ Email sending failed: {e}")
                    success = await self._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
                    # Check if it's a network error
                    error_str = str(e).lower()
                    if "network is unreachable" in error_str or "errno 101" in error_str or "timeout" in error_str:
                        return {
                            "success": False,
                            "message": f"Network connectivity issue detected: {str(e)}. The system cannot reach the Gmail SMTP server. Please check your network connection or try again later. Your report has been saved locally.",
                            "error": str(e),
                            "network_error": True
                        }
                    else:
                        return {
                            "success": False,
                            "message": f"Failed to send email: {str(e)}. Please check your email address and try again. Your report has been saved locally.",
                            "error": str(e)
                        }
        except Exception as e:
            print(f"⚠️ Email sending failed: {e}")
            success = await self._store_email_report_locally_async(recipient_email, prediction_data, patient_data)
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}. Please check your email address and try again.",
                "error": str(e)
            }
        finally:
            # Restore original timeout
            try:
                if 'original_timeout' in locals():
                    socket.setdefaulttimeout(original_timeout)
            except:
                pass
    
    def _send_email_sync_optimized(self, msg, recipient_email: str) -> Dict[str, Any]:
        """Optimized synchronous email sending with timeout control"""
        start_time = datetime.now()
        
        try:
            # Validate that we have required credentials
            if not self.sender_email or not self.sender_password:
                raise ValueError("Missing sender email or password")
                
            # Create optimized SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Use timeout on socket level
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.connection_timeout) as server:
                print("🔐 Starting TLS...")
                server.starttls(context=context)
                print("🔑 Logging in...")
                server.login(self.sender_email, self.sender_password)
                print("📧 Sending email...")
                
                server.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=[recipient_email],
                    msg=msg.as_string()
                )
            
            send_time = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Email sent in {send_time:.2f} seconds")
            
            return {"success": True, "send_time": f"{send_time:.2f}s"}
            
        except OSError as e:
            # Handle network connectivity issues specifically
            send_time = (datetime.now() - start_time).total_seconds()
            if hasattr(e, 'errno') and e.errno == 101:
                print(f"📡 Network connectivity issue after {send_time:.2f}s: {e}")
                print("💡 This may be due to:")
                print("   - Firewall restrictions")
                print("   - Network configuration issues")
                print("   - ISP blocking SMTP ports")
                print("   - Running in an environment with limited network access")
                raise Exception(f"Network connectivity issue: {str(e)}. The system cannot reach the Gmail SMTP server. Please check your network connection or try again later.")
            else:
                print(f"❌ Email send failed after {send_time:.2f}s: {e}")
                raise e
        except Exception as e:
            send_time = (datetime.now() - start_time).total_seconds()
            print(f"❌ Email send failed after {send_time:.2f}s: {e}")
            raise e
    
    async def _store_email_report_locally_async(self, recipient_email: str, prediction_data: Dict[str, Any], patient_data: Dict[str, Any]) -> bool:
        """Async version of local storage"""
        try:
            report = {
                "recipient": recipient_email,
                "prediction": prediction_data,
                "patient_data": patient_data,
                "timestamp": datetime.now().isoformat(),
                "status": "stored_locally"
            }
            
            # Use async file operations
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(None, self._store_report_sync, report)
            
            if success:
                print(f"✅ Email report stored locally for {recipient_email}")
            return success
            
        except Exception as e:
            print(f"❌ Failed to store email report locally: {e}")
            return False
    
    def _store_report_sync(self, report: Dict) -> bool:
        """Synchronous report storage"""
        try:
            reports_file = "email_reports.json"
            reports = []
            
            if os.path.exists(reports_file):
                try:
                    with open(reports_file, 'r') as f:
                        reports = json.load(f)
                except:
                    reports = []
            
            reports.append(report)
            
            # Keep only last 100 reports
            if len(reports) > 100:
                reports = reports[-100:]
            
            with open(reports_file, 'w') as f:
                json.dump(reports, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Sync storage failed: {e}")
            return False

# Global email service instance
fixed_email_service = FixedEmailService()