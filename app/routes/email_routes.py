from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.email import EmailCreate, EmailResponse
from app.services.email_service import send_email, get_received_emails
from app.database import get_db
from app.models.email import Email
from datetime import datetime

router = APIRouter(prefix="/emails", tags=["emails"])

@router.post("/send", response_model=EmailResponse)
def send_email_route(email: EmailCreate, db: Session = Depends(get_db)):
    return send_email(db, email.recipient, email.subject, email.body)

@router.get("/", response_model=list[EmailResponse])
def get_emails(
    direction: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(Email)
    if direction:
        query = query.filter(Email.direction == direction)
    if start_date:
        query = query.filter(Email.timestamp >= start_date)
    if end_date:
        query = query.filter(Email.timestamp <= end_date)
    return query.all()

@router.get("/statistics")
def get_statistics(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    sent_count = db.query(Email).filter(
        Email.direction == "sent",
        Email.timestamp.between(start_date, end_date)
    ).count()
    received_count = db.query(Email).filter(
        Email.direction == "received",
        Email.timestamp.between(start_date, end_date)
    ).count()
    return {"sent": sent_count, "received": received_count}