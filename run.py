import os
from flask import Flask
from src.routes import trigger
import logging

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(trigger.bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)