import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    
    # Appwrite Configuration
    APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT", "http://localhost/v1")
    APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID", "")
    APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY", "")
    APPWRITE_DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID", "default")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
