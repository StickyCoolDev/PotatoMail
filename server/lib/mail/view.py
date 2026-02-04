import os
import smtplib
from email.message import EmailMessage
from flask import Blueprint, request, jsonify

# 1. Import your database function
from dotenv import load_dotenv # <--- 1. Import this

load_dotenv() #
email_bp = Blueprint('email_bp', __name__)

from lib.db.repository import create_new_email 
API_KEY = os.getenv('API_AUTH_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

def send_email(sender_email, receiver_email, sender_password, subject, body_text, body_html=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msg.set_content(body_text)

    if body_html:
        msg.add_alternative(body_html, subtype='html')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

@email_bp.route('/send_email', methods=['POST'])
def handle_send_email():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No input data"}), 400

    subject = data.get('Subject')
    body_text = data.get('Body')
    body_html = data.get('Html Body')
    receiver_email = data.get('Receiver mail')

    if not all([subject, body_text, receiver_email]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    try:
        # 2. Send via SMTP
        send_email(
            sender_email=SENDER_EMAIL,
            receiver_email=receiver_email,
            sender_password=SENDER_PASSWORD,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )

        # 3. If SMTP succeeds, write to Database
        # Note: Your create_new_email function has its own try/except, 
        # so it won't crash the request if the DB is momentarily down.
        create_new_email(
            to_email=receiver_email,
            subject=subject,
            body=body_text,
            html_body=body_html
        )

        return jsonify({"status": "success", "message": "Email sent and logged to DB"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

