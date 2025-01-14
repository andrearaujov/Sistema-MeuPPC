# backend/app.py

from flask import Flask
from config import Config
from utils.database import mysql
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
