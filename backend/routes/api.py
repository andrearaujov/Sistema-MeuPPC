from flask import Blueprint, request, jsonify, redirect, url_for, make_response
from utils.database import mysql
from flask_cors import cross_origin
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from MySQLdb import Error, cursors
import datetime
from flask_mysqldb import MySQL, cursors
from config import Config
import MySQLdb.cursors
from models.pessoaCrud import PessoaCRUD
from models.ppcCRUD import PPCCrud
from models.relatorio import Relatorio
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
        ppcs_em_criacao = [ppc for ppc in ppcs if ppc.status == 'Em Criacao']  # Filtra PPCs em criação
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
            for ppc in ppcs_em_criacao
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
        user_role = decoded_token['papel']

        cursor = mysql.connection.cursor()

        # Permitir que coordenadores e colaboradores editem os PPCs
        if user_role == 'Coordenador':
            query = "UPDATE ppc SET titulo = %s, descricao = %s WHERE id = %s AND coordenador_id = %s"
            cursor.execute(query, (titulo, descricao, ppc_id, user_id))
        elif user_role == 'Colaborador':
            query = """
                UPDATE ppc p
                INNER JOIN ppc_colaboradores pc ON p.id = pc.ppc_id
                SET p.titulo = %s, p.descricao = %s
                WHERE p.id = %s AND pc.colaborador_id = %s
            """
            cursor.execute(query, (titulo, descricao, ppc_id, user_id))
        else:
            return jsonify({'error': 'Usuário não autorizado'}), 403

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

        cursor = mysql.connection.cursor(cursors.DictCursor)

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
        return jsonify({'message': 'PPC enviado para avaliação com sucesso', 'redirect_url': '/dashboard'}), 200

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
        
        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*, GROUP_CONCAT(ppc_colaboradores.colaborador_id) as colaboradores
            FROM ppc
            INNER JOIN ppc_colaboradores ON ppc.id = ppc_colaboradores.ppc_id
            WHERE ppc_colaboradores.colaborador_id = %s
            GROUP BY ppc.id
            ORDER BY ppc.created_at DESC  -- Ordena pelos mais recentes
        """
        cursor.execute(query, (colaborador_id,))
        resultados = cursor.fetchall()
        cursor.close()
        
        print(f"Resultados da consulta: {resultados}")  # Log de depuração
        
        ppcs = [PPC(**resultado) for resultado in resultados]
        for ppc in ppcs:
            if ppc.colaboradores:
                ppc.colaboradores = ppc.colaboradores.split(',')  # Converter string para lista
            else:
                ppc.colaboradores = []

        # Remover o atributo 'estrategia' antes de serializar
        ppcs_serializaveis = []
        for ppc in ppcs:
            ppc_dict = ppc.__dict__
            if 'estrategia' in ppc_dict:
                del ppc_dict['estrategia']
            ppcs_serializaveis.append(ppc_dict)

        print(f"PPCs serializáveis: {ppcs_serializaveis}")  # Log de depuração
        
        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        print(f"Erro interno do servidor: {str(e)}")  # Log do erro
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@api_bp.route('/avaliadores/ppcs', methods=['GET'])
def listar_ppcs_avaliador():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']
        
        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*, GROUP_CONCAT(ppc_avaliadores.avaliador_id) as avaliadores
            FROM ppc
            INNER JOIN ppc_avaliadores ON ppc.id = ppc_avaliadores.ppc_id
            WHERE ppc_avaliadores.avaliador_id = %s
            GROUP BY ppc.id
            ORDER BY ppc.created_at DESC  -- Ordena pelos mais recentes
        """
        cursor.execute(query, (avaliador_id,))
        resultados = cursor.fetchall()
        cursor.close()

        print(f"Resultados da consulta: {resultados}")  # Log de depuração

        ppcs = []
        for resultado in resultados:
            resultado.pop('avaliadores', None)  # Remove o campo avaliadores antes de criar a instância
            ppc = PPC(**resultado)
            ppcs.append(ppc)

        # Remover o atributo 'estrategia' antes de serializar
        ppcs_serializaveis = []
        for ppc in ppcs:
            ppc_dict = ppc.__dict__
            if 'estrategia' in ppc_dict:
                del ppc_dict['estrategia']
            ppcs_serializaveis.append(ppc_dict)

        print(f"PPCs serializáveis: {ppcs_serializaveis}")  # Log de depuração

        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        print(f"Erro interno do servidor: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@api_bp.route('/ppcs/<int:ppc_id>/avaliacao', methods=['POST'])
def salvar_avaliacao(ppc_id):
    data = request.get_json()
    avaliacao = data.get('evaluation')
    comentarios = data.get('comments')

    if not avaliacao:
        return jsonify({'error': 'A avaliação é obrigatória'}), 400

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']

        cursor = mysql.connection.cursor()
        
        if avaliacao == 'aprovado':
            query = "UPDATE ppc SET status = 'Aprovado', motivo_rejeicao = NULL WHERE id = %s"
            cursor.execute(query, (ppc_id,))
        elif avaliacao == 'desaprovado':
            query = "UPDATE ppc SET status = 'Rejeitado', motivo_rejeicao = %s WHERE id = %s"
            cursor.execute(query, (comentarios, ppc_id))
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Avaliação salva com sucesso'}), 201
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Error as e:
        return jsonify({'error': f'Erro ao salvar avaliação: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/avaliadores/ppcs/nao_avaliados', methods=['GET'])
def listar_ppcs_nao_avaliados():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']

        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*
            FROM ppc
            INNER JOIN ppc_avaliadores ON ppc.id = ppc_avaliadores.ppc_id
            WHERE ppc_avaliadores.avaliador_id = %s AND ppc.status = 'Em Avaliacao'
            GROUP BY ppc.id
            ORDER BY ppc.created_at DESC
        """
        cursor.execute(query, (avaliador_id,))
        resultados = cursor.fetchall()
        cursor.close()

        ppcs_serializaveis = [resultado for resultado in resultados]
        
        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500
@api_bp.route('/avaliadores/ppcs/avaliados', methods=['GET'])
def listar_ppcs_avaliados():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']

        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*
            FROM ppc
            INNER JOIN ppc_avaliadores ON ppc.id = ppc_avaliadores.ppc_id
            WHERE ppc_avaliadores.avaliador_id = %s AND ppc.status IN ('Aprovado', 'Rejeitado')
            GROUP BY ppc.id
            ORDER BY ppc.created_at DESC
        """
        cursor.execute(query, (avaliador_id,))
        resultados = cursor.fetchall()
        cursor.close()

        ppcs_serializaveis = [resultado for resultado in resultados]
        
        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/colaboradores/ppcs_avaliados', methods=['GET'])
def listar_ppcs_avaliados_colaboradores():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        colaborador_id = decoded_token['id']

        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*
            FROM ppc
            INNER JOIN ppc_colaboradores ON ppc.id = ppc_colaboradores.ppc_id
            WHERE ppc_colaboradores.colaborador_id = %s AND ppc.status IN ('Aprovado', 'Rejeitado')
            GROUP BY ppc.id
            ORDER BY ppc.created_at DESC
        """
        cursor.execute(query, (colaborador_id,))
        resultados = cursor.fetchall()
        cursor.close()

        ppcs_serializaveis = [resultado for resultado in resultados]
        
        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/coordenadores/ppcs_avaliados', methods=['GET'])
def listar_ppcs_avaliados_coordenadores():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        coordenador_id = decoded_token['id']

        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT ppc.*
            FROM ppc
            WHERE ppc.coordenador_id = %s AND ppc.status IN ('Aprovado', 'Rejeitado')
            ORDER BY ppc.created_at DESC
        """
        cursor.execute(query, (coordenador_id,))
        resultados = cursor.fetchall()
        cursor.close()

        ppcs_serializaveis = [resultado for resultado in resultados]
        
        return jsonify(ppcs_serializaveis), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500







logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@api_bp.route('/perfil', methods=['GET'])
def perfil():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error('Cabeçalho de autorização não encontrado')
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['id']

        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = "SELECT id, nome, email FROM pessoa WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            logger.error(f'Usuário não encontrado: {user_id}')
            return jsonify({'error': 'Usuário não encontrado'}), 404

        logger.info(f'Perfil do usuário carregado: {user}')
        return jsonify(user), 200
    except jwt.ExpiredSignatureError:
        logger.error('Token expirado')
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        logger.error('Token inválido')
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        logger.error(f'Erro interno do servidor: {e}')
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/ppcs/<int:ppc_id>/relatorio_colaboradores', methods=['GET'])
def relatorio_colaboradores(ppc_id):
    ppc = PPCCrud.buscar_por_id(ppc_id)
    if ppc:
        relatorio = Relatorio(ppc)
        colaboradores = relatorio.gerarRelatorioColaboradores()
        return jsonify(colaboradores), 200
    return jsonify({'error': 'PPC não encontrado'}), 404

@api_bp.route('/ppcs/<int:ppc_id>/relatorio_avaliadores', methods=['GET'])
def relatorio_avaliadores(ppc_id):
    ppc = PPCCrud.buscar_por_id(ppc_id)
    if ppc:
        relatorio = Relatorio(ppc)
        avaliadores = relatorio.gerarRelatorioAvaliadores()
        return jsonify(avaliadores), 200
    return jsonify({'error': 'PPC não encontrado'}), 404

@api_bp.route('/ppcs/<int:ppc_id>/relatorio_participantes', methods=['GET'])
def relatorio_participantes(ppc_id):
    ppc = PPCCrud.buscar_por_id(ppc_id)
    if ppc:
        relatorio = Relatorio(ppc)
        participantes = relatorio.gerarRelatorioParticipantes()
        return jsonify(participantes), 200
    return jsonify({'error': 'PPC não encontrado'}), 404

@api_bp.route('/ppcs_avaliados', methods=['GET'])
def listar_todos_ppcs_avaliados():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        
        cursor = mysql.connection.cursor(cursors.DictCursor)
        query = """
            SELECT * FROM ppc WHERE status IN ('Aprovado', 'Rejeitado')
            ORDER BY created_at DESC
        """
        cursor.execute(query)
        ppcs = cursor.fetchall()
        cursor.close()

        return jsonify(ppcs), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500


@api_bp.route('/avaliadores/ppcs/<int:ppc_id>/aprovar', methods=['POST'])
def aprovar_ppc(ppc_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']

        # Lógica para aprovar o PPC
        cursor = mysql.connection.cursor()
        query = "UPDATE ppc SET status = 'Aprovado' WHERE id = %s"
        cursor.execute(query, (ppc_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'PPC aprovado com sucesso'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500

@api_bp.route('/avaliadores/ppcs/<int:ppc_id>/rejeitar', methods=['POST'])
def rejeitar_ppc(ppc_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error('Cabeçalho de autorização não encontrado')
        return jsonify({'error': 'Cabeçalho de autorização não encontrado'}), 401

    try:
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        avaliador_id = decoded_token['id']

        data = request.get_json()
        descricao = data.get('descricao')
        logger.info(f'Requisição de rejeição recebida para PPC {ppc_id} com a descrição: {descricao}')

        if not descricao:
            logger.error('Descrição de rejeição não fornecida')
            return jsonify({'error': 'Descrição de rejeição não fornecida'}), 400

        # Lógica para rejeitar o PPC e adicionar a descrição
        cursor = mysql.connection.cursor()
        query = "UPDATE ppc SET status = 'Rejeitado', motivo_rejeicao = %s WHERE id = %s"
        cursor.execute(query, (descricao, ppc_id))
        mysql.connection.commit()
        cursor.close()

        logger.info(f'PPC {ppc_id} rejeitado com sucesso com a descrição: {descricao}')
        return jsonify({'message': 'PPC rejeitado com sucesso'}), 200
    except jwt.ExpiredSignatureError:
        logger.error('Token expirado')
        return jsonify({'error': 'Token expirado, por favor faça login novamente'}), 401
    except jwt.InvalidTokenError:
        logger.error('Token inválido')
        return jsonify({'error': 'Token inválido, por favor faça login novamente'}), 401
    except Exception as e:
        logger.error(f'Erro interno do servidor: {e}')
        return jsonify({'error': f'Erro interno do servidor: {e}'}), 500



# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@api_bp.route('/ppcs/delete', methods=['POST'])
def deletar_ppc_post():
    logger.debug("Iniciando o processo de exclusão do PPC")
    data = request.get_json()
    ppc_id = data.get('ppc_id')
    logger.debug(f"ID do PPC recebido: {ppc_id}")

    token = request.headers.get('Authorization')
    if not token:
        logger.error("Erro: Token ausente!")
        return jsonify({'error': 'Token ausente!'}), 401

    try:
        token_clean = token.split(" ")[1]  # Remover 'Bearer' do token
        logger.debug(f"Token limpo: {token_clean}")

        # Decodificar o token JWT
        decoded_token = jwt.decode(token_clean, Config.SECRET_KEY, algorithms=["HS256"])
        user_role = decoded_token['papel']
        logger.debug(f"Token decodificado. Papel do usuário: {user_role}")
        logger.debug(f"Token decodificado: {decoded_token}")

        if user_role != 'Coordenador':
            logger.error("Erro: Usuário não é coordenador.")
            return jsonify({'error': 'Acesso negado: Apenas coordenadores podem realizar esta ação!'}), 403

        cursor = mysql.connection.cursor()
        cursor.callproc('delete_ppc', [ppc_id])
        mysql.connection.commit()
        cursor.close()
        logger.debug("PPC excluído com sucesso")
        return jsonify({'message': 'PPC excluído com sucesso'})
    except Error as db_error:
        logger.error(f"Erro ao excluir PPC (DB): {str(db_error)}")
        return jsonify({'error': str(db_error)}), 500
    except Exception as e:
        logger.error(f"Erro ao excluir PPC: {str(e)}")
        return jsonify({'error': str(e)}), 500
