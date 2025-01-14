from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Lógica de autenticação de teste
    if username == "seuUsuario" and password == "suaSenha":
        return jsonify({"message": "Login bem-sucedido", "username": username})
    else:
        return jsonify({"error": "Credenciais inválidas"}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # Lógica de registro de teste
    # Normalmente você verificaria se o usuário já existe, salvando no banco de dados, etc.
    return jsonify({"message": "Usuário registrado com sucesso", "name": name, "email": email})

if __name__ == '__main__':
    app.run(port=5000)
