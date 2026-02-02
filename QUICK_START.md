# Quick Start Guide

## 1. Install Dependencies
```bash
uv sync
```

## 2. Configure Appwrite
```bash
cp .env.example .env
# Edit .env with your Appwrite credentials
```

## 3. Create Collections
```bash
uv run python setup_appwrite.py
```

Or using the bash script:
```bash
bash setup_appwrite.sh
```

## 4. Run the Application
```bash
uv run python run.py
```

Visit http://localhost:5000 in your browser.

## 5. Register and Use
1. Go to http://localhost:5000/auth/register to create an account
2. Login at http://localhost:5000/auth/login
3. Go to http://localhost:5000/auth/dashboard to generate an API key
4. Configure your SMTP credentials in Appwrite console
5. Start sending emails using the API

## Send Email Example
```bash
curl -X POST http://localhost:5000/send_email \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": "test@example.com",
    "subject": "Hello",
    "message": "This is a test email"
  }'
```

For detailed documentation, see [AUTH_SETUP.md](AUTH_SETUP.md).
