"""
Email Sender Service
Handles actual email sending operations.
Currently logs to console, designed for easy integration with email providers.
"""
from typing import Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Service for sending emails"""
    
    @staticmethod
    async def send_email(
        to: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> dict:
        """
        Send an email to a recipient.
        
        Args:
            to: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body (optional)
            
        Returns:
            Dict with status and message
            
        TODO: Replace with actual email service (choose one):
        
        Option 1 - SendGrid:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email='noreply@yourapp.com',
                to_emails=to,
                subject=subject,
                html_content=html_body
            )
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            
        Option 2 - Mailgun:
            import requests
            
            response = requests.post(
                f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                auth=("api", MAILGUN_API_KEY),
                data={
                    "from": "noreply@yourapp.com",
                    "to": to,
                    "subject": subject,
                    "html": html_body,
                    "text": text_body
                }
            )
            
        Option 3 - SMTP (Nodemailer equivalent in Python):
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'noreply@yourapp.com'
            msg['To'] = to
            
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail('noreply@yourapp.com', to, msg.as_string())
        """
        
        # MOCK EMAIL SENDER - Console logging for demo
        timestamp = datetime.utcnow().isoformat()
        
        logger.info("=" * 80)
        logger.info(f"📧 SENDING EMAIL - {timestamp}")
        logger.info("=" * 80)
        logger.info(f"To: {to}")
        logger.info(f"Subject: {subject}")
        logger.info("-" * 80)
        logger.info("HTML Body:")
        logger.info(html_body[:500] + "..." if len(html_body) > 500 else html_body)
        if text_body:
            logger.info("-" * 80)
            logger.info("Text Body:")
            logger.info(text_body[:300] + "..." if len(text_body) > 300 else text_body)
        logger.info("=" * 80)
        
        return {
            "status": "sent",
            "message": f"Email sent to {to}",
            "timestamp": timestamp
        }
    
    @staticmethod
    async def send_bulk_emails(
        recipients: list,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> dict:
        """
        Send emails to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body
            
        Returns:
            Dict with send results
        """
        results = {
            "success": [],
            "failed": []
        }
        
        for recipient in recipients:
            try:
                result = await EmailSender.send_email(recipient, subject, html_body, text_body)
                results["success"].append({
                    "email": recipient,
                    "timestamp": result["timestamp"]
                })
            except Exception as e:
                logger.error(f"Failed to send email to {recipient}: {str(e)}")
                results["failed"].append({
                    "email": recipient,
                    "error": str(e)
                })
        
        return results
