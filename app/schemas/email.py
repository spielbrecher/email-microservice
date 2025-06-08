from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmailCreate(BaseModel):
    recipient: str
    subject: str
    body: str

class EmailResponse(EmailCreate):
    id: str
    timestamp: datetime
    direction: str

    class Config:
        orm_mode = True