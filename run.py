import os
from dotenv import load_dotenv, find_dotenv

# load the .env from the repo root (if present) before importing app/create_app
load_dotenv(find_dotenv(), override=True)

from app import create_app


def main():
    config = os.environ.get("POTATOMAIL_CONFIG", "app.config.DevelopmentConfig")
    app = create_app(config)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
