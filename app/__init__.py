from flask import Flask
from dotenv import load_dotenv, find_dotenv
from app.mail_service.view import mail_service_bp
from app.auth.view import auth_bp

# ensure we load the project's .env reliably
load_dotenv(find_dotenv(), override=True)


def create_app(config_object: str = "app.config.Config") -> Flask:
    """App factory. Pass a config path like 'app.config.DevelopmentConfig'."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.config.from_object(config_object)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(mail_service_bp)

    @app.route("/")
    def index():
        return "PotatoMail is running"

    return app
