import smtplib

from email.message import EmailMessage

def send_email(sender_email, receiver_email, sender_password, subject, body):
    # 1. Create the message container
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    try:
        # 2. Connect to Gmail's SMTP server
        # Port 587 is standard for STARTTLS
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Secure the connection
            
            # 3. Login and send
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

