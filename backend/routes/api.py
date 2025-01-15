from flask import Blueprint, request, jsonify
from utils.database import mysql
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config
import MySQLdb.cursors
from models.pessoaCrud import PessoaCRUD
from models.ppcCRUD import PPCCrud
from models.ppc import PPC
import logging

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Instâncias dos CRUDs
pessoa_crud = PessoaCRUD()
ppc_crud = PPCCrud()

# Rotas de usuário (registro e login)
@api_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    papel = data.get('papel')

    if not nome or not email or not password or not papel:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pessoa WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        return jsonify({'error': 'E-mail já registrado'}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO pessoa (nome, email, senha, papel) VALUES (%s, %s, %s, %s)",
                   (nome, email, hashed_password, papel))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201



@api_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

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
        
        print(f"Usuário logado com sucesso: ID={user['id']}, Papel={user['papel']}")

        return jsonify({'message': 'Login realizado com sucesso', 'token': token}), 200

    return jsonify({'error': 'Credenciais inválidas'}), 401


# Rotas de PPC


# Configure o logger
logging.basicConfig(filename='app.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')



@api_bp.route('/ppcs', methods=['POST'])
def create_ppc():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        coordenador_id = decoded_token['id']
        papel = decoded_token['papel']
        print(f"Token decodificado: ID={coordenador_id}, Papel={papel}")

        if papel != 'Coordenador':
            return jsonify({'error': 'Usuário não é um Coordenador'}), 403

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except IndexError:
        return jsonify({'error': 'Formato do cabeçalho de autorização inválido'}), 401

    try:
        coordenador = pessoa_crud.buscar_por_id(coordenador_id)
        if not coordenador or coordenador.papel != 'Coordenador':
            print("Erro: Coordenador não encontrado ou inválido.")
            return jsonify({'error': 'Coordenador não encontrado ou inválido'}), 400

        ppc = ppc_crud.criar(titulo, descricao, coordenador_id)
        if ppc:
            print("PPC criado com sucesso.")
            # Certifique-se de que o retorno seja serializável em JSON
            ppc_dict = {
                'id': ppc.id,
                'titulo': ppc.titulo,
                'descricao': ppc.descricao,
                'status': ppc.status,
                'coordenador_id': ppc.coordenador_id,
                'colaboradores': ppc.colaboradores,
                'avaliadores': ppc.avaliadores
            }
            return jsonify({'message': 'PPC criado com sucesso', 'ppc': ppc_dict}), 201
        else:
            print("Erro ao criar PPC.")
        return jsonify({'error': 'Erro ao criar PPC'}), 500
    except Exception as e:
        print(f"Erro interno do servidor: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@api_bp.route('/ppcs/<int:ppc_id>', methods=['GET'])
def get_ppc(ppc_id):
    try:
        ppc = ppc_crud.buscar_por_id(ppc_id)
        if ppc:
            # Certifique-se de retornar dados serializáveis em JSON
            ppc_dict = {
                'id': ppc.id,
                'titulo': ppc.titulo,
                'descricao': ppc.descricao,
                'status': ppc.status,
                'coordenador_id': ppc.coordenador_id,
                'colaboradores': ppc.colaboradores,
                'avaliadores': ppc.avaliadores
            }
            return jsonify(ppc_dict), 200
        else:
            return jsonify({'error': 'PPC não encontrado'}), 404
    except Exception as e:
        print(f"Erro interno do servidor: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@api_bp.route('/ppcs', methods=['GET'])
def list_ppcs():
    try:
        ppcs = ppc_crud.listar_todos()
        ppcs_dict = [
            {
                'id': ppc.id,
                'titulo': ppc.titulo,
                'descricao': ppc.descricao,
                'status': ppc.status,
                'coordenador_id': ppc.coordenador_id,
                'colaboradores': ppc.colaboradores,
                'avaliadores': ppc.avaliadores
            } for ppc in ppcs
        ]
        return jsonify(ppcs_dict), 200
    except Exception as e:
        print(f"Erro interno do servidor: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

