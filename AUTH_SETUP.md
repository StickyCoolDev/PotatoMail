# PotatoMail Authentication System

This document explains how to set up and use the authentication system in PotatoMail.

## Overview

PotatoMail now includes a complete authentication system powered by Appwrite. Users can:

1. **Register & Login** - Create accounts via a web dashboard
2. **Generate API Keys** - Create personal API keys for programmatic email sending
3. **Manage SMTP Credentials** - Store their Gmail/email credentials securely
4. **Send Emails** - Use API keys to send authenticated emails

## Architecture

```
┌─────────────────┐
│ Web Dashboard   │ (Jinja2 + Alpine.js)
│ (/auth/*)       │
└────────┬────────┘
         │ Session Auth
         │
┌────────▼────────┐      ┌──────────────────┐
│  Flask Routes   │◄────►│   Appwrite DB    │
│  - Register     │      │   - Users        │
│  - Login        │      │   - API Keys     │
│  - Dashboard    │      │   - SMTP Config  │
└────────┬────────┘      └──────────────────┘
         │ API Key Auth
         │
┌────────▼────────────────┐
│  Email API              │
│  POST /send_email       │
│  (requires API key)     │
└─────────────────────────┘
```

## Setup Instructions

### 1. Install Dependencies

```bash
uv sync
```

This installs the Appwrite Python SDK along with other dependencies.

### 2. Set Up Appwrite

#### Option A: Self-hosted Appwrite

```bash
docker run -d \
  --name appwrite \
  -p 80:80 \
  -p 443:443 \
  appwrite/appwrite:latest
```

Then access the console at `http://localhost` and create a project.

#### Option B: Appwrite Cloud

Sign up at [cloud.appwrite.io](https://cloud.appwrite.io) and create a project.

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Appwrite credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
# Appwrite Configuration
APPWRITE_ENDPOINT=http://localhost:80/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key
APPWRITE_DATABASE_ID=default
```

### 4. Create Appwrite Collections

You can use the automated setup script to create all collections:

```bash
uv run python setup_appwrite.py
```

This script will:
- Connect to your Appwrite instance
- Create the `api_keys` collection
- Create the `smtp_configs` collection
- Set up all required attributes and indexes

**Manual Setup (Alternative)**

If you prefer to create collections manually, you need to create these two collections in your Appwrite database:

#### Collection 1: `api_keys`

Attributes:
- `user_id` (string, required)
- `name` (string, required)
- `key` (string, required, indexed)
- `status` (string, required, default: "active")
- `created_at` (string, required)
- `last_used` (string, nullable)

#### Collection 2: `smtp_configs`

Attributes:
- `sender_email` (string, required)
- `password` (string, required)

**Note:** In production, consider encrypting the password field.

### 5. Run the Application

```bash
uv run python run.py
```

The app will start on `http://localhost:5000`

## User Workflows

### Registration & Login

1. Visit `http://localhost:5000/auth/register`
2. Create an account with email and password
3. After registration, login at `http://localhost:5000/auth/login`

### Generate API Key

1. After login, go to `/auth/dashboard`
2. Scroll to "API Keys" section
3. Click "Create New Key"
4. Give it a name (e.g., "Production", "Development")
5. **Save the key** - you won't see it again!

### Configure SMTP Credentials

Once logged in, users need to configure their SMTP credentials:

1. In the dashboard, add a document to the `smtp_configs` collection with:
   - `sender_email`: The email address to send from (e.g., your Gmail)
   - `password`: The app-specific password or email password

**For Gmail users:**
- Enable 2-factor authentication
- Generate an [App Password](https://myaccount.google.com/apppasswords)
- Use the App Password in the configuration

### Send Emails via API

Once you have an API key and SMTP configured:

```bash
curl -X POST http://localhost:5000/send_email \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": "recipient@example.com",
    "subject": "Hello World",
    "message": "This is a test email",
    "email_type": "text"
  }'
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `receiver_email` | string | Yes | Email address to send to |
| `subject` | string | Yes | Email subject line |
| `message` | string | Yes | Email body content |
| `email_type` | string | No | `text`, `html`, `enriched`, `markdown`, or `xml` (default: `text`) |

**Response:**

Success:
```json
{
  "message": "Email sent successfully"
}
```

Error:
```json
{
  "error": "Error description"
}
```

## Authentication Methods

### Web Dashboard (Session-based)

- Uses Flask sessions with secure cookies
- Cookies are `HttpOnly`, `Secure`, and `SameSite`
- Protected by `@login_required` decorator
- Expires automatically based on browser session

### Email API (API Key-based)

- Requires `X-API-Key` header or `api_key` query parameter
- Protected by `@api_key_required` decorator
- Validates against `api_keys` collection
- Can be revoked from dashboard

## File Structure

```
app/
├── __init__.py              # App factory with Blueprint registration
├── config.py                # Configuration with Appwrite settings
├── auth/
│   ├── __init__.py          # Appwrite client initialization
│   └── view.py              # Auth routes and decorators
├── mail_service/
│   ├── __init__.py          # Email sending logic
│   └── view.py              # Email endpoint (now requires API key)
├── templates/               # Jinja2 templates
│   ├── base.html            # Base template with navbar
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   └── dashboard.html       # API key management dashboard
└── static/
    └── style.css            # Stylesheet for all pages
```

## Frontend Technologies

- **Jinja2**: Server-side template rendering
- **Alpine.js**: Lightweight JavaScript framework for interactivity
- **Custom CSS**: Clean, responsive design

## Security Considerations

1. **Passwords**: Hash with Appwrite (uses bcrypt)
2. **API Keys**: 32-character random strings (UUID format)
3. **SMTP Passwords**: Stored in database (encrypt in production)
4. **Sessions**: Secure, HttpOnly cookies
5. **HTTPS**: Required for production deployments

## API Key Management

- **List Keys**: `GET /auth/api/keys`
- **Create Key**: `POST /auth/api/keys` with `{"name": "key-name"}`
- **Revoke Key**: `DELETE /auth/api/keys/<key-id>`

## Troubleshooting

### "API key required" error

Make sure you're including the API key in your request:

```bash
curl -H "X-API-Key: YOUR_KEY" ...
```

### "SMTP configuration not found"

Configure your SMTP credentials in the Appwrite `smtp_configs` collection before trying to send emails.

### "Invalid API key"

Check that:
1. The key exists in the database
2. The key status is "active" (not "revoked")
3. You're using the correct key value

### Appwrite connection errors

Verify:
1. Appwrite server is running
2. `APPWRITE_ENDPOINT` is correct
3. `APPWRITE_PROJECT_ID` and `APPWRITE_API_KEY` are valid
4. Your firewall allows connections to Appwrite

## Next Steps

- Deploy to Render.com, Heroku, or your preferred platform
- Set up HTTPS certificates for production
- Configure a proper database for SMTP credential encryption
- Add rate limiting to prevent abuse
- Implement email verification for new accounts
- Add password reset functionality
