from dotenv import load_dotenv
import os

load_dotenv()

from app.mail_service import EmailSendStatus, send_email, EmailTypes


def test_send_email():
    # Test sending an email
    test_html_content = """
    <html>
        <body>
            <h1>This is a test HTML email</h1>
            <p>If you can see this, the HTML email was sent successfully!</p>
        </body>
    </html>
    """
    result = send_email(
        os.getenv("TEST_EMAIL"),
        os.getenv("TEST_RECEIVER"),
        os.getenv("TEST_PASSWORD"),
        test_html_content,
        "Test Subject",
        email_type=EmailTypes.HTML,
    )
    if result["status"] != EmailSendStatus.SUCCESS:
        raise Exception("Failed to send email", result.get("error"))


if __name__ == "__main__":
    test_send_email()
    print("Email sent successfully.")
