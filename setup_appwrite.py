#!/usr/bin/env python3
"""
Setup script to create Appwrite collections for PotatoMail.

This script creates the necessary collections and attributes in your Appwrite database.
It reads credentials from environment variables or .env file.

Usage:
    python setup_appwrite.py
"""

import os
import sys
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()
    return {
        "endpoint": os.getenv("APPWRITE_ENDPOINT", "http://localhost:80/v1"),
        "project_id": os.getenv("APPWRITE_PROJECT_ID"),
        "api_key": os.getenv("APPWRITE_API_KEY"),
        "database_id": os.getenv("APPWRITE_DATABASE_ID", "default"),
    }


def validate_config(config):
    """Validate that all required config values are present."""
    if not config["project_id"]:
        print("❌ Error: APPWRITE_PROJECT_ID not set in .env")
        sys.exit(1)
    if not config["api_key"]:
        print("❌ Error: APPWRITE_API_KEY not set in .env")
        sys.exit(1)
    print("✓ Configuration loaded successfully")
    print(f"  Endpoint: {config['endpoint']}")
    print(f"  Project ID: {config['project_id']}")
    print(f"  Database ID: {config['database_id']}")


def get_database_client(config):
    """Initialize and return Appwrite client and database service."""
    client = Client()
    client.set_endpoint(config["endpoint"])
    client.set_project(config["project_id"])
    client.set_key(config["api_key"])
    db = Databases(client)
    return db


def create_api_keys_collection(db, database_id):
    """Create the api_keys collection."""
    print("\n📦 Creating 'api_keys' collection...")
    
    try:
        # Create collection
        collection = db.create_collection(
            database_id=database_id,
            collection_id="api_keys",
            name="API Keys",
            permissions=[],  # Permissions handled at attribute level
        )
        print("  ✓ Collection created")
        
        # Create attributes - note: don't set default for required attributes
        attributes = [
            {
                "name": "user_id",
                "type": "string",
                "size": 256,
                "required": True,
            },
            {
                "name": "name",
                "type": "string",
                "size": 256,
                "required": True,
            },
            {
                "name": "key",
                "type": "string",
                "size": 256,
                "required": True,
            },
            {
                "name": "status",
                "type": "string",
                "size": 50,
                "required": True,
                "default": "active",
            },
            {
                "name": "created_at",
                "type": "string",
                "size": 50,
                "required": True,
            },
            {
                "name": "last_used",
                "type": "string",
                "size": 50,
                "required": False,
            },
        ]
        
        for attr in attributes:
            try:
                kwargs = {
                    "database_id": database_id,
                    "collection_id": "api_keys",
                    "key": attr["name"],
                    "size": attr["size"],
                    "required": attr["required"],
                }
                if "default" in attr:
                    kwargs["default"] = attr["default"]
                
                db.create_string_attribute(**kwargs)
                print(f"  ✓ Attribute '{attr['name']}' created")
            except AppwriteException as e:
                if "already exists" in str(e):
                    print(f"  ⚠ Attribute '{attr['name']}' already exists")
                else:
                    raise
        
        # Create index on key field for faster queries
        try:
            db.create_index(
                database_id=database_id,
                collection_id="api_keys",
                key="key_index",
                type="key",
                attributes=["key"],
                orders=["ASC"],
            )
            print("  ✓ Index on 'key' field created")
        except AppwriteException as e:
            if "already exists" in str(e):
                print("  ⚠ Index on 'key' field already exists")
            else:
                raise
        
        print("✅ 'api_keys' collection setup complete")
        
    except AppwriteException as e:
        if "already exists" in str(e):
            print("⚠ 'api_keys' collection already exists")
        else:
            print(f"❌ Error creating 'api_keys' collection: {e}")
            raise


def create_smtp_configs_collection(db, database_id):
    """Create the smtp_configs collection."""
    print("\n📦 Creating 'smtp_configs' collection...")
    
    try:
        # Create collection
        collection = db.create_collection(
            database_id=database_id,
            collection_id="smtp_configs",
            name="SMTP Configurations",
            permissions=[],
        )
        print("  ✓ Collection created")
        
        # Create attributes - don't set default for required attributes
        attributes = [
            {
                "name": "sender_email",
                "type": "string",
                "size": 256,
                "required": True,
            },
            {
                "name": "password",
                "type": "string",
                "size": 512,
                "required": True,
            },
        ]
        
        for attr in attributes:
            try:
                kwargs = {
                    "database_id": database_id,
                    "collection_id": "smtp_configs",
                    "key": attr["name"],
                    "size": attr["size"],
                    "required": attr["required"],
                }
                if "default" in attr:
                    kwargs["default"] = attr["default"]
                
                db.create_string_attribute(**kwargs)
                print(f"  ✓ Attribute '{attr['name']}' created")
            except AppwriteException as e:
                if "already exists" in str(e):
                    print(f"  ⚠ Attribute '{attr['name']}' already exists")
                else:
                    raise
        
        print("✅ 'smtp_configs' collection setup complete")
        
    except AppwriteException as e:
        if "already exists" in str(e):
            print("⚠ 'smtp_configs' collection already exists")
        else:
            print(f"❌ Error creating 'smtp_configs' collection: {e}")
            raise


def main():
    """Main setup function."""
    print("=" * 60)
    print("PotatoMail Appwrite Collections Setup")
    print("=" * 60)
    
    # Load and validate configuration
    print("\n🔧 Loading configuration...")
    config = load_env()
    validate_config(config)
    
    # Initialize database client
    print("\n🔗 Connecting to Appwrite...")
    try:
        db = get_database_client(config)
        print("✓ Connected successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Appwrite: {e}")
        print("   Check your APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, and APPWRITE_API_KEY")
        sys.exit(1)
    
    # Create collections
    try:
        create_api_keys_collection(db, config["database_id"])
        create_smtp_configs_collection(db, config["database_id"])
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Appwrite collections setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: uv run python run.py")
    print("2. Visit: http://localhost:5000/auth/register")
    print("3. Create an account and generate an API key")
    print("4. Configure your SMTP credentials in the Appwrite console")
    print("\nFor more information, see AUTH_SETUP.md")


if __name__ == "__main__":
    main()
