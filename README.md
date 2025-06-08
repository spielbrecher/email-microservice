# Email Microservice

FastAPI-микросервис для отправки и получения электронных писем с использованием Mailpit и PostgreSQL. Предоставляет REST API для управления почтовыми операциями.

---

## Основные возможности
- Отправка писем через SMTP (Mailpit)
- Получение писем через Mailpit REST API
- Статистика отправленных/полученных писем
- Фильтрация писем по дате и направлению

---

## Технологии
- FastAPI
- Mailpit
- PostgreSQL
- Docker/Docker Compose
- SQLAlchemy

---

## Установка

### Предварительные требования
- [Docker](https://www.docker.com/)  (v20.10+)
- Git

### Шаги установки

git clone https://github.com/spielbrecher/email-microservice.git

cd email-microservice

docker-compose up -d

## Тестирование

### Проверка статуса 

docker-compose ps

#### Ожидаемые контейнеры:

email_microservice-app-1 (FastAPI)

email_microservice-db-1 (PostgreSQL)

email_microservice-mailpit-1 (Mailpit)

### Ручной запуск тестов в контейнере:

#### Войдите в контейнер
docker exec -it email_microservice-app-1 /bin/sh

#### Перейдите в рабочую директорию
cd /app

#### Запустите тесты
pytest tests/ -v

#### Ожидаемые результаты
collected 3 items

tests/test_emails.py::test_send_email PASSED

tests/test_emails.py::test_get_emails PASSED

tests/test_emails.py::test_get_statistics PASSED
