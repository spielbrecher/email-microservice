import smtplib
from email.message import EmailMessage
import uuid
from datetime import datetime
import requests
from app.config import settings
from app.models.email import Email, EmailDirection
from sqlalchemy.orm import Session

def send_email(db: Session, recipient: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.MAILPIT_SENDER
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(settings.MAILPIT_SMTP_HOST, settings.MAILPIT_SMTP_PORT) as smtp:
        smtp.send_message(msg)

    email_entry = Email(
        id=str(uuid.uuid4()),
        subject=subject,
        body=body,
        sender=settings.MAILPIT_SENDER,
        recipient=recipient,
        timestamp=datetime.utcnow(),
        direction=EmailDirection.sent
    )
    db.add(email_entry)
    db.commit()
    db.refresh(email_entry)
    return email_entry

def get_received_emails(db: Session):
    try:
        response = requests.get(f"{settings.MAILPIT_API_URL}/api/v1/messages")
        response.raise_for_status()
        messages = response.json().get("messages", [])
        emails = []

        for msg in messages:
            email_entry = Email(
                id=msg["id"],
                subject=msg["fromMail"],
                body=msg["text"],
                sender=msg["fromMail"],
                recipient=", ".join(msg["toMails"]),
                timestamp=datetime.fromisoformat(msg["createdAt"]),
                direction=EmailDirection.received
            )
            db.add(email_entry)
            emails.append(email_entry)
        db.commit()
        return emails
    except Exception as e:
        db.rollback()
        raise e