from flask import Flask
import sys
import os
sys.path.append(os.getcwd())
from dotenv import load_dotenv

from lib.mail.view import email_bp
load_dotenv()
app = Flask(__name__)


app.register_blueprint(email_bp)

if __name__ == "__main__":
    app.run("0.0.0.0", port=2000)
