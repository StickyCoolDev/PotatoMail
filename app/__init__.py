from flask import Flask
from dotenv import load_dotenv, find_dotenv

# ensure we load the project's .env reliably
load_dotenv(find_dotenv(), override=True)


def create_app(config_object: str = "app.config.Config") -> Flask:
    """App factory. Pass a config path like 'app.config.DevelopmentConfig'."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    @app.route("/")
    def index():
        print(app.config.get("SECRET_KEY"))  ## only for test
        return "PotatoMail is running"

    return app
