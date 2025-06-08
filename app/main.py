from fastapi import FastAPI
from app.routes import email_routes
from app.database import engine, get_db
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import get_received_emails
from app.database import SessionLocal
from app.models.email import Email  
from app.database.base import Base  

app = FastAPI(title="Email Microservice")

# Подключение маршрутов
app.include_router(email_routes.router)

# Инициализация БД
@app.on_event("startup")
def startup_event():
    from app.models.email import Email
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)
    # Запуск фонового задачника
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: get_received_emails(SessionLocal()), 'interval', minutes=1)
    scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Email Microservice is running"}