from flask import Flask, request
from config import Config
from utils.database import mysql
from routes.api import api_bp
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuração do CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir todas as origens para fins de desenvolvimento

    mysql.init_app(app)
    app.register_blueprint(api_bp)

    # Configuração de logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    @app.before_request
    def log_request_info():
        logger.info(f'Requisição recebida: {request.method} {request.url}')
        logger.info(f'Cabeçalhos: {request.headers}')
        logger.info(f'Corpo: {request.get_data()}')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
