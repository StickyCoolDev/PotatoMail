from flask import Blueprint, request, jsonify
from app.mail_service import send_email, EmailTypes
from email_validator import validate_email, EmailNotValidError

mail_service_bp = Blueprint("mail_service", __name__)

"""
route : /send_email
this route is mapped to the internal send_email function.
expects: application/json
"""


@mail_service_bp.route("/send_email", methods=["POST"])
def send_email_route():

    data = request.json
    sender_email = data.get("sender_email")
    receiver_email = data.get("receiver_email")
    password = data.get("password")
    message = data.get("message")
    subject = data.get("subject")
    email_type_str = data.get("email_type", "text").upper()

    try:
        validate_email(sender_email)
    except EmailNotValidError as e:
        return jsonify({"error": "Invalid sender email"}), 400

    try:
        validate_email(receiver_email)
    except EmailNotValidError as e:
        return jsonify({"error": "Invalid receiver email"}), 400

    try:
        email_type = EmailTypes[email_type_str]
    except KeyError:
        return jsonify({"error": "Invalid email type"}), 400

    result = send_email(
        sender_email, receiver_email, password, message, subject, email_type
    )

    if result["status"] == "success":
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": str(result.get("error"))}), 500
