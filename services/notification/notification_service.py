"""
LABBAIK AI v6.0 - Notification Service
======================================
Handles email, WhatsApp, and in-app notifications.
"""

from __future__ import annotations
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum
import json

from core.config import get_settings
from core.exceptions import EmailServiceError, ExternalServiceError

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & DATA CLASSES
# =============================================================================

class NotificationChannel(str, Enum):
    """Notification channels."""
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"
    PUSH = "push"


class NotificationPriority(str, Enum):
    """Notification priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class NotificationType(str, Enum):
    """Notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    BOOKING = "booking"
    PAYMENT = "payment"
    REMINDER = "reminder"
    PROMOTION = "promotion"
    WELCOME = "welcome"
    VERIFICATION = "verification"


@dataclass
class NotificationMessage:
    """Notification message data."""
    recipient_id: str
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None
    
    channel: NotificationChannel = NotificationChannel.EMAIL
    type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.NORMAL
    
    subject: str = ""
    title: str = ""
    body: str = ""
    html_body: Optional[str] = None
    
    data: Dict[str, Any] = field(default_factory=dict)
    template_id: Optional[str] = None
    
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class NotificationResult:
    """Notification send result."""
    success: bool
    message_id: Optional[str] = None
    channel: Optional[NotificationChannel] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# EMAIL TEMPLATES
# =============================================================================

class EmailTemplates:
    """Email template definitions."""
    
    BASE_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #1B4D3E 0%, #2E7D32 100%);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                background: #fff;
                padding: 30px;
                border: 1px solid #e0e0e0;
            }}
            .footer {{
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-radius: 0 0 8px 8px;
            }}
            .button {{
                display: inline-block;
                background: #1B4D3E;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 4px;
                margin: 10px 0;
            }}
            .highlight {{
                background: #f0f7f4;
                padding: 15px;
                border-left: 4px solid #1B4D3E;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🕋 LABBAIK AI</h1>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>© 2024 LABBAIK AI - Asisten Perjalanan Umrah Cerdas</p>
            <p>Powered by MS Hadianto</p>
        </div>
    </body>
    </html>
    """
    
    WELCOME = """
    <h2>Assalamu'alaikum, {name}! 🌙</h2>
    <p>Selamat datang di <strong>LABBAIK AI</strong> - platform cerdas untuk membantu 
    perjalanan ibadah Umrah Anda.</p>
    
    <div class="highlight">
        <strong>Fitur yang bisa Anda nikmati:</strong>
        <ul>
            <li>💬 Tanya jawab seputar Umrah dengan AI</li>
            <li>🧮 Simulasi biaya perjalanan</li>
            <li>📖 Panduan lengkap ibadah Umrah</li>
            <li>👥 Temukan partner perjalanan</li>
        </ul>
    </div>
    
    <p>
        <a href="{app_url}" class="button">Mulai Sekarang</a>
    </p>
    
    <p>Semoga Allah SWT memudahkan perjalanan ibadah Anda. Aamiin.</p>
    """
    
    VERIFICATION = """
    <h2>Verifikasi Email Anda</h2>
    <p>Halo {name},</p>
    <p>Terima kasih telah mendaftar di LABBAIK AI. Silakan klik tombol di bawah 
    untuk memverifikasi alamat email Anda:</p>
    
    <p style="text-align: center;">
        <a href="{verification_url}" class="button">Verifikasi Email</a>
    </p>
    
    <p><small>Link ini akan kedaluwarsa dalam 24 jam.</small></p>
    
    <p>Jika Anda tidak mendaftar di LABBAIK AI, abaikan email ini.</p>
    """
    
    BOOKING_CONFIRMATION = """
    <h2>Konfirmasi Booking Anda</h2>
    <p>Halo {name},</p>
    <p>Terima kasih telah melakukan booking di LABBAIK AI.</p>
    
    <div class="highlight">
        <strong>Detail Booking:</strong>
        <p>
            <strong>Nomor Booking:</strong> {booking_number}<br>
            <strong>Tanggal Berangkat:</strong> {departure_date}<br>
            <strong>Kota Keberangkatan:</strong> {departure_city}<br>
            <strong>Jumlah Jamaah:</strong> {traveler_count} orang<br>
            <strong>Total:</strong> Rp {total_price}
        </p>
    </div>
    
    <p>
        <a href="{booking_url}" class="button">Lihat Detail Booking</a>
    </p>
    
    <p>Tim kami akan segera menghubungi Anda untuk proses selanjutnya.</p>
    """
    
    PAYMENT_REMINDER = """
    <h2>Pengingat Pembayaran</h2>
    <p>Halo {name},</p>
    <p>Ini adalah pengingat untuk melakukan pembayaran booking Anda:</p>
    
    <div class="highlight">
        <strong>Nomor Booking:</strong> {booking_number}<br>
        <strong>Jumlah:</strong> Rp {amount}<br>
        <strong>Batas Waktu:</strong> {due_date}
    </div>
    
    <p>
        <a href="{payment_url}" class="button">Bayar Sekarang</a>
    </p>
    
    <p><small>Booking akan otomatis dibatalkan jika pembayaran tidak dilakukan 
    sebelum batas waktu.</small></p>
    """
    
    PASSWORD_RESET = """
    <h2>Reset Password</h2>
    <p>Halo {name},</p>
    <p>Kami menerima permintaan untuk reset password akun LABBAIK AI Anda.</p>
    
    <p style="text-align: center;">
        <a href="{reset_url}" class="button">Reset Password</a>
    </p>
    
    <p><small>Link ini akan kedaluwarsa dalam 1 jam.</small></p>
    
    <p>Jika Anda tidak meminta reset password, abaikan email ini.</p>
    """


# =============================================================================
# BASE NOTIFICATION SENDER
# =============================================================================

class BaseNotificationSender(ABC):
    """Abstract base for notification senders."""
    
    @property
    @abstractmethod
    def channel(self) -> NotificationChannel:
        """Return channel type."""
        pass
    
    @abstractmethod
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send notification."""
        pass
    
    @abstractmethod
    def send_batch(self, messages: List[NotificationMessage]) -> List[NotificationResult]:
        """Send batch notifications."""
        pass


# =============================================================================
# EMAIL SENDER
# =============================================================================

class EmailSender(BaseNotificationSender):
    """Email notification sender using SMTP."""
    
    def __init__(
        self,
        smtp_host: str = None,
        smtp_port: int = None,
        smtp_user: str = None,
        smtp_password: str = None,
        from_address: str = None,
        use_tls: bool = True
    ):
        settings = get_settings()
        
        self.smtp_host = smtp_host or os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.environ.get("SMTP_USER", "")
        self.smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD", "")
        self.from_address = from_address or os.environ.get("EMAIL_FROM", "noreply@labbaik.cloud")
        self.use_tls = use_tls
        
        self._templates = EmailTemplates()
    
    @property
    def channel(self) -> NotificationChannel:
        return NotificationChannel.EMAIL
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """
        Send email notification.
        
        Args:
            message: Notification message
        
        Returns:
            NotificationResult
        """
        if not message.recipient_email:
            return NotificationResult(
                success=False,
                channel=self.channel,
                error="Recipient email is required"
            )
        
        try:
            # Create email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = message.subject or message.title
            msg["From"] = self.from_address
            msg["To"] = message.recipient_email
            
            # Add plain text
            msg.attach(MIMEText(message.body, "plain"))
            
            # Add HTML if available
            if message.html_body:
                html_content = self._templates.BASE_TEMPLATE.format(
                    content=message.html_body
                )
                msg.attach(MIMEText(html_content, "html"))
            
            # Send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                
                server.sendmail(
                    self.from_address,
                    message.recipient_email,
                    msg.as_string()
                )
            
            logger.info(f"Email sent to {message.recipient_email}")
            
            return NotificationResult(
                success=True,
                channel=self.channel,
                message_id=f"email_{datetime.utcnow().timestamp()}"
            )
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return NotificationResult(
                success=False,
                channel=self.channel,
                error=f"SMTP error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Email send error: {e}")
            return NotificationResult(
                success=False,
                channel=self.channel,
                error=str(e)
            )
    
    def send_batch(self, messages: List[NotificationMessage]) -> List[NotificationResult]:
        """Send batch emails."""
        results = []
        for msg in messages:
            results.append(self.send(msg))
        return results
    
    def send_template(
        self,
        template_name: str,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        **template_vars
    ) -> NotificationResult:
        """
        Send email using template.
        
        Args:
            template_name: Template name (welcome, verification, etc.)
            recipient_email: Recipient email
            recipient_name: Recipient name
            subject: Email subject
            **template_vars: Template variables
        
        Returns:
            NotificationResult
        """
        template_map = {
            "welcome": self._templates.WELCOME,
            "verification": self._templates.VERIFICATION,
            "booking_confirmation": self._templates.BOOKING_CONFIRMATION,
            "payment_reminder": self._templates.PAYMENT_REMINDER,
            "password_reset": self._templates.PASSWORD_RESET,
        }
        
        template = template_map.get(template_name)
        if not template:
            return NotificationResult(
                success=False,
                error=f"Unknown template: {template_name}"
            )
        
        # Render template
        template_vars["name"] = recipient_name
        html_body = template.format(**template_vars)
        
        # Create message
        message = NotificationMessage(
            recipient_id="",
            recipient_email=recipient_email,
            subject=subject,
            title=subject,
            body=f"Email for {recipient_name}",
            html_body=html_body,
            type=NotificationType.INFO,
        )
        
        return self.send(message)


# =============================================================================
# IN-APP NOTIFICATION SENDER
# =============================================================================

class InAppNotificationSender(BaseNotificationSender):
    """In-app notification sender."""
    
    def __init__(self, notification_repository=None):
        self.repo = notification_repository
    
    @property
    def channel(self) -> NotificationChannel:
        return NotificationChannel.IN_APP
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """
        Save notification to database for in-app display.
        
        Args:
            message: Notification message
        
        Returns:
            NotificationResult
        """
        try:
            notification_data = {
                "user_id": message.recipient_id,
                "type": message.type.value,
                "title": message.title,
                "message": message.body,
                "link": message.data.get("link"),
                "is_read": False,
                "created_at": datetime.utcnow(),
            }
            
            if self.repo:
                result = self.repo.create(notification_data)
                notification_id = result.id
            else:
                # In-memory for demo
                notification_id = f"notif_{datetime.utcnow().timestamp()}"
            
            logger.info(f"In-app notification created for user {message.recipient_id}")
            
            return NotificationResult(
                success=True,
                channel=self.channel,
                message_id=notification_id
            )
            
        except Exception as e:
            logger.error(f"In-app notification error: {e}")
            return NotificationResult(
                success=False,
                channel=self.channel,
                error=str(e)
            )
    
    def send_batch(self, messages: List[NotificationMessage]) -> List[NotificationResult]:
        """Send batch in-app notifications."""
        results = []
        for msg in messages:
            results.append(self.send(msg))
        return results


# =============================================================================
# NOTIFICATION SERVICE
# =============================================================================

class NotificationService:
    """
    Main notification service.
    Handles routing to appropriate channels.
    """
    
    _instance: Optional["NotificationService"] = None
    
    def __new__(cls) -> "NotificationService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._senders: Dict[NotificationChannel, BaseNotificationSender] = {}
        self._initialized = True
        
        # Register default senders
        self.register_sender(EmailSender())
        self.register_sender(InAppNotificationSender())
    
    def register_sender(self, sender: BaseNotificationSender):
        """Register a notification sender."""
        self._senders[sender.channel] = sender
        logger.info(f"Registered notification sender: {sender.channel.value}")
    
    def send(
        self,
        message: NotificationMessage,
        channels: List[NotificationChannel] = None
    ) -> Dict[NotificationChannel, NotificationResult]:
        """
        Send notification through specified channels.
        
        Args:
            message: Notification message
            channels: Channels to send through (defaults to message.channel)
        
        Returns:
            Dict of results per channel
        """
        channels = channels or [message.channel]
        results = {}
        
        for channel in channels:
            sender = self._senders.get(channel)
            if sender:
                results[channel] = sender.send(message)
            else:
                results[channel] = NotificationResult(
                    success=False,
                    channel=channel,
                    error=f"No sender registered for {channel.value}"
                )
        
        return results
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: str = None,
        **kwargs
    ) -> NotificationResult:
        """
        Convenience method for sending email.
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Plain text body
            html: HTML body (optional)
        
        Returns:
            NotificationResult
        """
        message = NotificationMessage(
            recipient_id="",
            recipient_email=to,
            channel=NotificationChannel.EMAIL,
            subject=subject,
            title=subject,
            body=body,
            html_body=html,
            **kwargs
        )
        
        results = self.send(message)
        return results.get(NotificationChannel.EMAIL)
    
    def send_welcome_email(self, email: str, name: str, app_url: str = "https://labbaik.cloud") -> NotificationResult:
        """Send welcome email to new user."""
        sender = self._senders.get(NotificationChannel.EMAIL)
        if isinstance(sender, EmailSender):
            return sender.send_template(
                "welcome",
                recipient_email=email,
                recipient_name=name,
                subject="Selamat Datang di LABBAIK AI! 🕋",
                app_url=app_url
            )
        return NotificationResult(success=False, error="Email sender not available")
    
    def send_verification_email(self, email: str, name: str, verification_url: str) -> NotificationResult:
        """Send email verification."""
        sender = self._senders.get(NotificationChannel.EMAIL)
        if isinstance(sender, EmailSender):
            return sender.send_template(
                "verification",
                recipient_email=email,
                recipient_name=name,
                subject="Verifikasi Email LABBAIK AI",
                verification_url=verification_url
            )
        return NotificationResult(success=False, error="Email sender not available")
    
    def send_booking_confirmation(
        self,
        email: str,
        name: str,
        booking_number: str,
        departure_date: str,
        departure_city: str,
        traveler_count: int,
        total_price: str,
        booking_url: str
    ) -> NotificationResult:
        """Send booking confirmation email."""
        sender = self._senders.get(NotificationChannel.EMAIL)
        if isinstance(sender, EmailSender):
            return sender.send_template(
                "booking_confirmation",
                recipient_email=email,
                recipient_name=name,
                subject=f"Konfirmasi Booking {booking_number} - LABBAIK AI",
                booking_number=booking_number,
                departure_date=departure_date,
                departure_city=departure_city,
                traveler_count=traveler_count,
                total_price=total_price,
                booking_url=booking_url
            )
        return NotificationResult(success=False, error="Email sender not available")
    
    def notify_user(
        self,
        user_id: str,
        title: str,
        message: str,
        type: NotificationType = NotificationType.INFO,
        link: str = None
    ) -> NotificationResult:
        """
        Send in-app notification to user.
        
        Args:
            user_id: Target user ID
            title: Notification title
            message: Notification body
            type: Notification type
            link: Optional action link
        
        Returns:
            NotificationResult
        """
        msg = NotificationMessage(
            recipient_id=user_id,
            channel=NotificationChannel.IN_APP,
            type=type,
            title=title,
            body=message,
            data={"link": link} if link else {}
        )
        
        results = self.send(msg)
        return results.get(NotificationChannel.IN_APP)


def get_notification_service() -> NotificationService:
    """Get notification service singleton."""
    return NotificationService()


# Need to import os for environment variables
import os
