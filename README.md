# IMEI Checker Backend System with Telegram Bot Integration

## 1. Общие сведения

Этот проект представляет собой бэкенд-систему для проверки IMEI устройств. Система включает в себя интеграцию с Telegram-ботом, который позволяет пользователям проверять валидность IMEI номеров, а также предоставляет API для внешних запросов.

## 2. Функционал

### 2.1 Доступ
В Telegram-боте реализован список пользователей, для которых доступен функционал бота. Только пользователи из этого списка могут взаимодействовать с ботом.
Для доступа к API системы требуется авторизация через токен. Токен должен быть передан в заголовке запроса для получения доступа к функционалу.

### 2.2 Telegram-бот

**Отправка IMEI в Telegram-бот**:  
Пользователи могут отправить IMEI номер в бот, и он выполнит следующие действия:

- Проверит валидность IMEI.
- Отправит пользователю информацию о статусе IMEI, например, информацию о производителе или модели устройства.

### Пример использования API:

```bash
curl -X POST http://localhost:8000/api/check-imei \
     -H "Authorization: Bearer <your_token>" \
     -d '{"imei": "123456789012345"}'
```

## 3. Установка и настройка

### 3.1 Установка зависимостей

Для установки всех необходимых зависимостей используйте следующую команду:

```bash
pip install -r requirements.txt
```

Создайте файл .env в корне проекта и добавьте следующие параметры:
```
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=your_db_password_here

# Secret keys for authentication
SECRET_AUTH=your_secret_auth_key_here
SECRET_KEY=your_secret_key_here

# Telegram bot token
BOT_TOKEN=your_telegram_bot_token_here

# App URL
APP_URL=http://localhost:8000/

# IMEI API configuration
IMEI_API_TOKEN=your_imei_api_token_here
IMEI_API_URL=https://api.imeicheck.net/v1/checks
```

### 3.2 Запуск проекта
Для запуска API-сервиса используйте команду:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Для запуска Telegram-бота:

```bash
python src/bot.py
```
