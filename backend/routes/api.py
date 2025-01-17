from flask import Blueprint, request, jsonify
from utils.database import mysql
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from MySQLdb import Error
import datetime
from config import Config
import MySQLdb.cursors
from models.pessoaCrud import PessoaCRUD
from models.ppcCRUD import PPCCrud
from MySQLdb.cursors import DictCursor
from models.ppc import PPC
import logging

api_bp = Blueprint('api', __name__, url_prefix='/api')
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
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
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['id']

        ppcs = ppc_crud.listar_por_usuario(user_id)  # Novo método para listar PPCs do usuário
        ppcs_dict = [
            {
                'id': ppc.id,
                'titulo': ppc.titulo,
                'descricao': ppc.descricao,
                'status': ppc.status,
                'coordenador_id': ppc.coordenador_id,
                'colaboradores': ppc.colaboradores,
                'avaliadores': ppc.avaliadores
            }
            for ppc in ppcs
        ]
        return jsonify(ppcs_dict), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except IndexError:
        return jsonify({'error': 'Formato do cabeçalho de autorização inválido'}), 401
    except Exception as e:
        print(f"Erro interno do servidor: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@api_bp.route('/ppcs/<int:ppc_id>', methods=['PUT'])
def update_ppc(ppc_id):
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['id']

        cursor = mysql.connection.cursor()
        query = "UPDATE ppc SET titulo = %s, descricao = %s WHERE id = %s AND coordenador_id = %s"
        cursor.execute(query, (titulo, descricao, ppc_id, user_id))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'error': 'PPC não encontrado ou usuário não autorizado'}), 404

        return jsonify({'message': 'PPC atualizado com sucesso'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Error as e:
        return jsonify({'error': f'Erro ao atualizar PPC: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500


@api_bp.route('/ppcs/<int:ppc_id>/colaboradores', methods=['POST'])
def add_colaborador(ppc_id):
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        logging.error('O e-mail é obrigatório')
        return jsonify({'error': 'O e-mail é obrigatório'}), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.error('Cabeçalho de autorização não encontrado')
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        coordenador_id = decoded_token['id']

        cursor = mysql.connection.cursor(DictCursor)

        # Verifique se o usuário logado é o coordenador do PPC
        query = "SELECT coordenador_id FROM ppc WHERE id = %s"
        cursor.execute(query, (ppc_id,))
        result = cursor.fetchone()

        if not result or result['coordenador_id'] != coordenador_id:
            cursor.close()
            logging.error('Usuário não autorizado ou PPC não encontrado')
            return jsonify({'error': 'Usuário não autorizado'}), 403

        # Buscar o colaborador pelo e-mail
        colaborador = pessoa_crud.buscar_por_email(email)
        if not colaborador:
            cursor.close()
            logging.error(f'Colaborador com o e-mail {email} não encontrado')
            return jsonify({'error': 'Colaborador não encontrado'}), 404

        # Adicionar log detalhado do colaborador encontrado
        logging.info(f'Colaborador encontrado: {colaborador.__dict__}')

        # Verificar se o papel da pessoa é 'colaborador'
        logging.info(f'Papel do colaborador: {colaborador.papel}')
        if colaborador.papel != 'Colaborador':
            cursor.close()
            logging.error(f'Usuário com o e-mail {email} não tem o papel de colaborador')
            return jsonify({'error': 'Usuário não tem o papel de colaborador'}), 403

        # Adicionar o colaborador ao PPC
        query = "INSERT INTO ppc_colaboradores (ppc_id, colaborador_id) VALUES (%s, %s)"
        cursor.execute(query, (ppc_id, colaborador.id))
        mysql.connection.commit()
        cursor.close()

        logging.info('Colaborador adicionado com sucesso')
        return jsonify({'message': 'Colaborador adicionado com sucesso'}), 201

    except jwt.ExpiredSignatureError:
        logging.error('Token expirado')
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        logging.error('Token inválido')
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Error as e:
        logging.error(f'Erro ao adicionar colaborador: {e}')
        return jsonify({'error': f'Erro ao adicionar colaborador: {e}'}), 500
    except Exception as e:
        logging.error(f'Erro interno do servidor: {e}')
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/ppcs/<int:ppc_id>/enviar_para_avaliacao', methods=['POST'])
def enviar_para_avaliacao(ppc_id):
    data = request.get_json()
    avaliadores_ids = data.get('avaliadores_ids')
    
    if not avaliadores_ids:
        logging.error('Os IDs dos avaliadores são obrigatórios')
        return jsonify({'error': 'Os IDs dos avaliadores são obrigatórios'}), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.error('Cabeçalho de autorização não encontrado')
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        coordenador_id = decoded_token['id']

        cursor = mysql.connection.cursor(DictCursor)

        # Verifique se o usuário logado é o coordenador do PPC
        query = "SELECT coordenador_id FROM ppc WHERE id = %s"
        cursor.execute(query, (ppc_id,))
        result = cursor.fetchone()

        if not result or result['coordenador_id'] != coordenador_id:
            cursor.close()
            logging.error('Usuário não autorizado ou PPC não encontrado')
            return jsonify({'error': 'Usuário não autorizado'}), 403

        # Enviar o PPC para avaliação
        ppc = PPCCrud.buscar_por_id(ppc_id)
        logging.info(f'PPC encontrado: {ppc.__dict__}')

        ppc.enviar_para_avaliacao(avaliadores_ids)
        PPCCrud.atualizar(mysql.connection, ppc_id, status=ppc.status)
        logging.info(f'Status atualizado para: {ppc.status}')

        # Inserir os avaliadores na tabela ppc_avaliadores
        query = "INSERT INTO ppc_avaliadores (ppc_id, avaliador_id) VALUES (%s, %s)"
        for avaliador_id in avaliadores_ids:
            cursor.execute(query, (ppc_id, avaliador_id))
        mysql.connection.commit()
        cursor.close()

        logging.info('PPC enviado para avaliação com sucesso')
        return jsonify({'message': 'PPC enviado para avaliação com sucesso'}), 200

    except jwt.ExpiredSignatureError:
        logging.error('Token expirado')
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        logging.error('Token inválido')
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Error as e:
        logging.error(f'Erro ao enviar para avaliação: {e}')
        return jsonify({'error': f'Erro ao enviar para avaliação: {e}'}), 500
    except Exception as e:
        logging.error(f'Erro interno do servidor: {e}')
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/colaboradores/ppcs', methods=['GET'])
def listar_ppcs_colaborador():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        colaborador_id = decoded_token['id']
        ppcs = PPCCrud.listar_por_colaborador(colaborador_id)
        return jsonify([ppc.__dict__ for ppc in ppcs]), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500
