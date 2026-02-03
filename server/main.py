from lib.mail.view import email_bp
from flask import Flask

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


app.register_blueprint(email_bp)

if __name__ == "__main__":
    app.run("0.0.0.0", port=2000)
