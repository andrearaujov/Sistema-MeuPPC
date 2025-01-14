# backend/routes/api.py

from flask import Blueprint, request, jsonify
from utils.database import mysql
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config
import MySQLdb.cursors

api_bp = Blueprint('api', __name__, url_prefix='/api/users')

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')  # Altera para 'password'

    if not nome or not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pessoa WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        return jsonify({'error': 'E-mail já registrado'}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO pessoa (nome, email, senha, papel) VALUES (%s, %s, %s, %s)",
                   (nome, email, hashed_password, 'Colaborador'))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  # Altera para 'password'

    if not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pessoa WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['senha'], password):
        token = jwt.encode({
            'id': user['id'],
            'papel': user['papel'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, Config.SECRET_KEY, algorithm='HS256')

        return jsonify({'message': 'Login realizado com sucesso', 'token': token}), 200

    return jsonify({'error': 'Credenciais inválidas'}), 401
