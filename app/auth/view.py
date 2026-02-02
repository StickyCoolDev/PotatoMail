"""Authentication routes and views."""

import json
import uuid
from functools import wraps
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from appwrite.exception import AppwriteException
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.id import ID
from appwrite.query import Query

from app.auth import get_appwrite_client, get_account_client, get_databases_client

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = session.get("session_id")
        user_id = session.get("user_id")
        if not session_id or not user_id:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def api_key_required(f):
    """Decorator to require valid API key for API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
        
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        # Validate API key
        try:
            client = get_appwrite_client()
            db = Databases(client)
            
            # Query API keys collection
            keys_response = db.list_documents(
                database_id=current_app.config["APPWRITE_DATABASE_ID"],
                collection_id="api_keys",
                queries=[f'key == "{api_key}"', 'status == "active"']
            )
            
            if len(keys_response.get("documents", [])) == 0:
                return jsonify({"error": "Invalid API key"}), 401
            
            key_doc = keys_response["documents"][0]
            request.api_key_user_id = key_doc["user_id"]
            request.api_key_id = key_doc["$id"]
            
        except Exception as e:
            return jsonify({"error": "API key validation failed"}), 500
        
        return f(*args, **kwargs)
    
    return decorated_function


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        name = data.get("name", "").strip()
        
        if not email or not password or not name:
            return jsonify({"error": "Email, password, and name are required"}), 400
        
        try:
            client = get_appwrite_client()
            account = Account(client)
            
            # Create user
            user = account.create(
                user_id=ID.unique(),
                email=email,
                password=password,
                name=name
            )
            
            return jsonify({"message": "User created successfully", "user_id": user["$id"]}), 201
            
        except AppwriteException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Registration failed"}), 500
    
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login a user."""
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        try:
            client = get_appwrite_client()
            account = Account(client)
            
            # Create session
            session_response = account.create_email_password_session(
                email=email,
                password=password
            )
            
            # Extract session ID and user ID from response
            session_id = session_response.get("$id", "")
            user_id = session_response.get("userId", "")
            
            if not session_id or not user_id:
                return jsonify({"error": "Failed to create session"}), 400
            
            # Store in Flask session
            session["session_id"] = session_id
            session["user_id"] = user_id
            
            return jsonify({"message": "Logged in successfully", "redirect": "/auth/dashboard"}), 200
            
        except AppwriteException as e:
            error_msg = str(e)
            return jsonify({"error": error_msg}), 401
        except Exception as e:
            return jsonify({"error": "Login failed"}), 500
    
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout a user."""
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """User dashboard."""
    return render_template("dashboard.html")


@auth_bp.route("/api/user", methods=["GET"])
@login_required
def get_user():
    """Get current user info."""
    try:
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID not found in session"}), 401
        
        client = get_appwrite_client()
        users = Users(client)
        user = users.get(user_id)
        
        return jsonify({
            "$id": user.get("$id"),
            "name": user.get("name"),
            "email": user.get("email"),
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/api/keys", methods=["GET"])
@login_required
def get_api_keys():
    """Get user's API keys."""
    try:
        user_id = session.get("user_id")
        client = get_appwrite_client()
        db = Databases(client)
        
        keys = db.list_documents(
            database_id=current_app.config["APPWRITE_DATABASE_ID"],
            collection_id="api_keys",
            queries=[
                Query.equal("user_id", user_id),
            ]
        )
        
        # Hide full key values in response
        documents = keys.get("documents", [])
        for doc in documents:
            doc["key"] = doc["key"][:8] + "..." if len(doc["key"]) > 8 else "***"
        
        return jsonify(documents), 200
        
    except Exception as e:
        print(f"Error fetching API keys: {e}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/api/keys", methods=["POST"])
@login_required
def create_api_key():
    """Create a new API key for the user."""
    try:
        user_id = session.get("user_id")
        data = request.get_json()
        key_name = data.get("name", "API Key").strip()
        
        if not key_name:
            return jsonify({"error": "Key name is required"}), 400
        
        client = get_appwrite_client()
        db = Databases(client)
        
        # Generate a random API key
        api_key = str(uuid.uuid4()).replace("-", "")
        
        # Store in database
        key_doc = db.create_document(
            database_id=current_app.config["APPWRITE_DATABASE_ID"],
            collection_id="api_keys",
            document_id=ID.unique(),
            data={
                "user_id": user_id,
                "name": key_name,
                "key": api_key,
                #"status": "active",
               
                # "last_used": None
            }
        )
        
        return jsonify({
            "id": key_doc["$id"],
            "name": key_doc["name"],
            "key": api_key,
            "created_at": key_doc["$createdAt"]
        }), 201
        
    except Exception as e:
        print(f"Error creating API key: {e}")
        return jsonify({"error": str(e)}), 500

# 6627e5cffa4149e6b8e412f6d5f169ca
@auth_bp.route("/api/keys/<key_id>", methods=["DELETE"])
@login_required
def revoke_api_key(key_id):
    """Revoke an API key."""
    try:
        user_id = session.get("user_id")
        client = get_appwrite_client()
        db = Databases(client)
        
        # Verify key belongs to user
        key_doc = db.get_document(
            database_id=current_app.config["APPWRITE_DATABASE_ID"],
            collection_id="api_keys",
            document_id=key_id
        )
        
        if key_doc.get("user_id") != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        # Update key status to revoked
        db.update_document(
            database_id=current_app.config["APPWRITE_DATABASE_ID"],
            collection_id="api_keys",
            document_id=key_id,
            data={"status": "revoked"}
        )
        
        return jsonify({"message": "API key revoked"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
