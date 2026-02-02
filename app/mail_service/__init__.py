import enum
import smtplib
from email.message import EmailMessage

class EmailTypes(enum.Enum):
    TEXT = "text"
    HTML = "html"
    ENRICHED = "enriched"
    """DEPRECATED: Use MARKDOWN instead"""

    MARKDOWN = "markdown" 
    XML = "xml"

class EmailSendStatus(enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"

def send_email(sender_email : str, receiver_email : str, password : str, message: str, subject : str, email_type : EmailTypes = EmailTypes.TEXT):
    """
    Send an email using smtp.
    """
    email_message = EmailMessage()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    if email_type == EmailTypes.HTML:
        email_message.set_content("Please turn on html to view this message") 
    

    email_message.add_alternative(message, subtype=email_type.value)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        try:
            server.send_message(email_message)
            return {"status": EmailSendStatus.SUCCESS}
        except smtplib.SMTPException as error:
            return {"status": EmailSendStatus.FAILED, "error": error}