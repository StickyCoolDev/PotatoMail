# Appwrite Setup Scripts

This project includes three setup scripts for creating Appwrite collections. Choose the one that works best for your system.

## Python Script (Recommended)

**File:** `setup_appwrite.py`

Works on all platforms (Windows, macOS, Linux).

### Usage
```bash
uv run python setup_appwrite.py
```

### Features
- Validates environment variables
- Connects to Appwrite server
- Creates both collections (`api_keys` and `smtp_configs`)
- Creates all required attributes
- Creates database indexes for faster queries
- Handles existing collections gracefully
- Shows detailed progress and error messages

### Output Example
```
============================================================
PotatoMail Appwrite Collections Setup
============================================================

🔧 Loading configuration...
✓ Configuration loaded successfully
  Endpoint: http://localhost:80/v1
  Project ID: my-project-id
  Database ID: default

🔗 Connecting to Appwrite...
✓ Connected successfully

📦 Creating 'api_keys' collection...
  ✓ Collection created
  ✓ Attribute 'user_id' created
  ✓ Attribute 'name' created
  ✓ Attribute 'key' created
  ✓ Attribute 'status' created
  ✓ Attribute 'created_at' created
  ✓ Attribute 'last_used' created
  ✓ Index on 'key' field created
✅ 'api_keys' collection setup complete

📦 Creating 'smtp_configs' collection...
  ✓ Collection created
  ✓ Attribute 'sender_email' created
  ✓ Attribute 'password' created
✅ 'smtp_configs' collection setup complete

============================================================
✅ Appwrite collections setup complete!
============================================================
```

## Bash Script (Linux/macOS)

**File:** `setup_appwrite.sh`

Wrapper script for Unix-like systems.

### Usage
```bash
bash setup_appwrite.sh
```

Or make it executable and run directly:
```bash
chmod +x setup_appwrite.sh
./setup_appwrite.sh
```

### Features
- Validates `.env` file exists
- Checks if dependencies are installed
- Auto-installs dependencies if needed
- Runs the Python setup script

## Batch Script (Windows)

**File:** `setup_appwrite.bat`

Native Windows batch script.

### Usage
Double-click the file or run from Command Prompt:
```cmd
setup_appwrite.bat
```

### Features
- Validates `.env` file exists
- Checks if dependencies are installed
- Auto-installs dependencies if needed
- Runs the Python setup script
- Waits for user input before closing on error

## Before Running Any Script

1. **Copy .env template:**
   ```bash
   cp .env.example .env
   ```

2. **Fill in your Appwrite credentials in `.env`:**
   ```dotenv
   APPWRITE_ENDPOINT=http://localhost:80/v1
   APPWRITE_PROJECT_ID=your-project-id
   APPWRITE_API_KEY=your-api-key
   APPWRITE_DATABASE_ID=default
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

## Collections Created

The scripts automatically create:

### api_keys Collection
- `user_id` - Reference to the user
- `name` - Key friendly name
- `key` - The actual API key (32 chars)
- `status` - "active" or "revoked"
- `created_at` - ISO timestamp
- `last_used` - Last use timestamp (optional)

*Indexes:* `key` field is indexed for fast lookups

### smtp_configs Collection
- `sender_email` - Email address to send from
- `password` - SMTP password or app-specific password

## What if the script fails?

### Connection Error
- Verify Appwrite server is running
- Check `APPWRITE_ENDPOINT` is correct
- Ensure firewall allows connections

### Invalid Credentials
- Double-check `APPWRITE_PROJECT_ID`
- Verify `APPWRITE_API_KEY` is correct
- Confirm you're using the Server API Key, not a Client Key

### Collection Already Exists
- This is not an error; the script will skip creation
- You can safely run the script multiple times

## Manual Collection Creation

If you prefer to create collections manually through the Appwrite console:

1. Log in to your Appwrite console
2. Go to your database
3. Click "Create Collection"
4. For each collection, add the attributes listed above
5. Create an index on the `key` field in the `api_keys` collection

## Troubleshooting

### Python not found
- Ensure Python 3.12+ is installed
- Verify it's in your PATH

### Appwrite SDK not found
- Run `uv sync` to install dependencies
- The setup scripts do this automatically

### Permission denied (Linux/macOS)
```bash
chmod +x setup_appwrite.sh
```

### .env file not found
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Next Steps

After running the setup script:

1. Start the application:
   ```bash
   uv run python run.py
   ```

2. Visit http://localhost:5000

3. Create an account and generate an API key

4. Configure your SMTP credentials

5. Start sending emails!

See [QUICK_START.md](QUICK_START.md) for more details.
