from sqlalchemy import Column, String, Text, DateTime, Enum as SQLAlchemyEnum
from app.database.base import Base
from enum import Enum

class EmailDirection(str, Enum):
    sent = "sent"
    received = "received"

class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True)
    subject = Column(String)
    body = Column(Text)
    sender = Column(String)
    recipient = Column(String)
    timestamp = Column(DateTime)
    direction = Column(SQLAlchemyEnum(EmailDirection))