from flask import Blueprint, request, jsonify, current_app
from app.mail_service import send_email, EmailTypes
from app.auth.view import api_key_required
from email_validator import validate_email, EmailNotValidError
from appwrite.services.databases import Databases
from app.auth import get_appwrite_client

mail_service_bp = Blueprint("mail_service", __name__)

"""
route : /send_email
this route is mapped to the internal send_email function.
requires API key authentication
expects: application/json with receiver_email, message, subject, and optional email_type
"""


@mail_service_bp.route("/send_email", methods=["POST"])
@api_key_required
def send_email_route():
    """
    Send an email using an authenticated API key.
    
    Request body:
    {
        "receiver_email": "recipient@example.com",
        "message": "Email body",
        "subject": "Email subject",
        "email_type": "text" (optional, defaults to text)
    }
    """
    data = request.json
    receiver_email = data.get("receiver_email", "").strip()
    message = data.get("message", "").strip()
    subject = data.get("subject", "").strip()
    email_type_str = data.get("email_type", "text").upper()

    # Validate receiver email
    if not receiver_email:
        return jsonify({"error": "Receiver email is required"}), 400

    try:
        validate_email(receiver_email)
    except EmailNotValidError as e:
        return jsonify({"error": "Invalid receiver email"}), 400

    # Validate message and subject
    if not message:
        return jsonify({"error": "Message is required"}), 400

    if not subject:
        return jsonify({"error": "Subject is required"}), 400

    # Validate email type
    try:
        email_type = EmailTypes[email_type_str]
    except KeyError:
        return jsonify({"error": "Invalid email type"}), 400

    # Get user's SMTP credentials from Appwrite
    try:
        user_id = request.api_key_user_id
        client = get_appwrite_client()
        db = Databases(client)
        
        # Get user's SMTP configuration from database
        smtp_config = db.get_document(
            database_id=current_app.config["APPWRITE_DATABASE_ID"],
            collection_id="smtp_configs",
            document_id=user_id
        )
        
        sender_email = smtp_config.get("sender_email")
        password = smtp_config.get("password")
        
        if not sender_email or not password:
            return jsonify({"error": "SMTP configuration not found. Please configure your email settings in the dashboard."}), 400
        
    except Exception as e:
        return jsonify({"error": "Failed to retrieve SMTP configuration. Please configure your email settings in the dashboard."}), 400

    # Send email
    result = send_email(
        sender_email, receiver_email, password, message, subject, email_type
    )

    if result["status"] == "success":
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": str(result.get("error"))}), 500
