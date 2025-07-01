# 🧾 QR-Based Employee Registration & Authentication API

## 📚 Описание

Этот проект — это API-сервис на FastAPI, позволяющий:

- Регистрировать сотрудников через `POST /employees/` с возможностью загрузки фотографии.
- Генерировать уникальный QR-код для каждого сотрудника (`GET /employees/{id}/qr/`).
- Авторизоваться по QR-коду с помощью `POST /token/` (получение access token).
- Получать список сотрудников с их фотографиями через `GET /employees/` (защищён Bearer токеном).
- Использовать Swagger UI для тестирования API (/docs).

---

##  Эндпоинты

###  Регистрация сотрудника

**POST** `/employees/`

- Принимает:
    - `full_name` (строка)
    - `email` (строка)
    - `photo` (изображение — файл, опционально)
- Возвращает:
    - `id`, `full_name`, `email`, `photo_url`

---

###  Получение QR-кода сотрудника

**GET** `/employees/{employee_id}/qr/`

- Отдаёт HTML-страницу с QR-кодом сотрудника
- QR-код содержит access token

---

###  Авторизация по QR-коду

**POST** `/token/`

- Принимает:
    - `qr_token` (строка, извлекается из QR)
- Возвращает:
    - `access_token`, `token_type`

💡 Также есть Python-скрипт, который может:

- Сканировать изображение с QR-кодом
- Распознать токен decoode_qr.py
- Отправить его на `/token/` и получить access token

---

### ✅ Получение списка сотрудников

**GET** `/employees/`

- Защищён Bearer токеном
- Возвращает список сотрудников:
    - `id`, `full_name`, `email`, `photo_url`

---

## ⚙️ Технологии

- Python 3.9+
- FastAPI
- SQLite
- SQLAlchemy
- qrcode
- JWT
- Docker

---

## 🐳 Запуск через Docker

```bash
# Сборка образа
docker build -t myapp .

# Запуск контейнера
docker run -p 8000:8000 myapp
