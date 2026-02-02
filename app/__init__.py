from flask import Flask
from dotenv import load_dotenv, find_dotenv
from app.mail_service.view import mail_service_bp

# ensure we load the project's .env reliably
load_dotenv(find_dotenv(), override=True)


def create_app(config_object: str = "app.config.Config") -> Flask:
    """App factory. Pass a config path like 'app.config.DevelopmentConfig'."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(mail_service_bp)

    @app.route("/")
    def index():
        return "PotatoMail is running"

    return app
