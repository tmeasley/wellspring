"""
Email notification system for Wellspring Mountain
Sends notifications when staff create notes, maintenance tasks, etc.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

# Configuration
NOTIFICATION_EMAIL = "SpringMountainWellness@proton.me"
NOTIFICATION_PHONE = "743-241-6310"

def send_email_notification(
    subject: str,
    body: str,
    to_email: Optional[str] = None,
    note_type: str = "general"
) -> bool:
    """
    Send email notification for staff notes and activities

    Args:
        subject: Email subject line
        body: Email body content
        to_email: Optional recipient email (defaults to NOTIFICATION_EMAIL)
        note_type: Type of notification (property_note, maintenance, todo, etc.)

    Returns:
        True if email sent successfully, False otherwise

    Note:
        This is a stub function. To enable actual email sending:
        1. Set up SMTP credentials in .env file
        2. Configure SMTP settings below
        3. Uncomment the actual sending code
    """

    if to_email is None:
        to_email = NOTIFICATION_EMAIL

    # Log the notification (for now, since SMTP isn't configured)
    log_notification(subject, body, to_email, note_type)

    # TODO: Implement actual email sending when SMTP is configured
    # Uncomment below when ready:

    """
    try:
        # SMTP Configuration (add these to .env file)
        smtp_server = os.getenv("SMTP_SERVER", "smtp.protonmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")

        if not smtp_username or not smtp_password:
            print("SMTP credentials not configured. Email not sent.")
            return False

        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    """

    # For now, just log
    print(f"[EMAIL NOTIFICATION] {subject} - would send to {to_email}")
    return True

def log_notification(subject: str, body: str, to_email: str, note_type: str):
    """Log notification to file"""
    log_file = "notification_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Type: {note_type}\n")
        f.write(f"To: {to_email}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Body:\n{body}\n")
        f.write(f"{'='*60}\n")

def notify_property_note_created(unit_name: str, note_title: str, note_content: str, priority: str, created_by: str):
    """Send notification when a property note is created"""
    subject = f"New Property Note: {unit_name} - {note_title}"
    body = f"""
A new property note has been created for Wellspring Mountain.

Building/Area: {unit_name}
Note Title: {note_title}
Priority: {priority.upper()}
Created By: {created_by}
Created At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Note Content:
{note_content}

---
To view and manage this note, log into the Wellspring Mountain staff dashboard.

Contact: {NOTIFICATION_PHONE}
Email: {NOTIFICATION_EMAIL}
    """.strip()

    return send_email_notification(subject, body, note_type="property_note")

def notify_maintenance_task_created(unit_name: str, task_title: str, task_type: str, priority: str, scheduled_date: str):
    """Send notification when a maintenance task is created"""
    subject = f"New Maintenance Task: {unit_name} - {task_title}"
    body = f"""
A new maintenance task has been created for Wellspring Mountain.

Building/Area: {unit_name}
Task: {task_title}
Type: {task_type.replace('_', ' ').title()}
Priority: {priority.upper()}
Scheduled Date: {scheduled_date}
Created At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
To view and manage this task, log into the Wellspring Mountain staff dashboard under Property Management > Maintenance.

Contact: {NOTIFICATION_PHONE}
Email: {NOTIFICATION_EMAIL}
    """.strip()

    return send_email_notification(subject, body, note_type="maintenance")

def notify_booking_request(guest_name: str, booking_type: str, check_in: str, check_out: str, guests: int):
    """Send notification when a new booking request is received"""
    subject = f"New Booking Request: {guest_name} - {booking_type.title()}"
    body = f"""
A new booking request has been received for Wellspring Mountain.

Guest: {guest_name}
Booking Type: {booking_type.title()}
Check-in: {check_in}
Check-out: {check_out}
Number of Guests: {guests}
Request Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
To review and approve this booking, log into the Wellspring Mountain staff dashboard.

Contact: {NOTIFICATION_PHONE}
Email: {NOTIFICATION_EMAIL}
    """.strip()

    return send_email_notification(subject, body, note_type="booking")

def notify_road_maintenance_request(description: str, priority: str, requested_by: str):
    """Send notification for road maintenance requests"""
    subject = f"Road Maintenance Request - {priority.upper()} Priority"
    body = f"""
A road maintenance request has been submitted for Wellspring Mountain.

Priority: {priority.upper()}
Requested By: {requested_by}
Request Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Description:
{description}

---
To manage this request, log into the Wellspring Mountain staff dashboard under Property Management > Maintenance.

Contact: {NOTIFICATION_PHONE}
Email: {NOTIFICATION_EMAIL}
    """.strip()

    return send_email_notification(subject, body, note_type="road_maintenance")

# Configuration instructions
def print_email_setup_instructions():
    """Print instructions for setting up email notifications"""
    print("""
=================================================================
EMAIL NOTIFICATION SETUP INSTRUCTIONS
=================================================================

To enable email notifications, add these to your .env file:

SMTP_SERVER=smtp.protonmail.com
SMTP_PORT=587
SMTP_USERNAME=SpringMountainWellness@proton.me
SMTP_PASSWORD=your_app_password_here

For ProtonMail:
1. Log into ProtonMail
2. Go to Settings > Security
3. Enable "Less secure apps" or create an App Password
4. Use that password in SMTP_PASSWORD

Then uncomment the email sending code in utils/email_notifications.py

For now, all notifications are being logged to notification_log.txt

=================================================================
    """)

if __name__ == "__main__":
    print_email_setup_instructions()
