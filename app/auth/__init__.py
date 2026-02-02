"""Authentication module with Appwrite integration."""

from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from flask import current_app


def get_appwrite_client():
    """Initialize and return an Appwrite client."""
    client = Client()
    client.set_endpoint(current_app.config["APPWRITE_ENDPOINT"])
    client.set_project(current_app.config["APPWRITE_PROJECT_ID"])
    client.set_key(current_app.config["APPWRITE_API_KEY"])
    return client


def get_account_client(session_cookie=None):
    """Get an Appwrite Account client, optionally with a session cookie."""
    client = Client()
    client.set_endpoint(current_app.config["APPWRITE_ENDPOINT"])
    client.set_project(current_app.config["APPWRITE_PROJECT_ID"])
    if session_cookie:
        client.set_session(session_cookie)
    return client


def get_databases_client(session_cookie=None):
    """Get an Appwrite Databases client."""
    client = get_account_client(session_cookie)
    return Databases(client)
