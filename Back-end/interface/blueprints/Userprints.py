from flask import Blueprint, request, jsonify
from domain.entities.UserEntity import UserEntity as User
from application.services.UserService import UserService
from core.helpers.Criptograph import Criptograph
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

cripto = Criptograph()
service = UserService()

userprints = Blueprint('userprints', __name__)

@userprints.route('/create', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              description: Nome do usuário
            email:
              type: string
              format: email
              description: E-mail do usuário
            password:
              type: string
              format: password
              description: Senha do usuário (mínimo 6 caracteres)
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User created successfully"
      400:
        description: Entrada inválida
      405:
        description: Método não permitido
      500:
        description: Erro interno do servidor
    """
    try:
        if request.method != 'POST':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data = request.get_json()
        user_entity = User(
            username=data.get('name'),
            email=data.get('email'),
            password=cripto.hash_password(data.get('password')),
            is_active=True
        )
        
        service.create_user(user_entity)
        
        return jsonify({"message": "User created successfully"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@userprints.route('/login', methods=['POST'])
def login_user():
    """
    Autentica um usuário e retorna um token JWT
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              description: E-mail do usuário
            password:
              type: string
              format: password
              description: Senha do usuário
    responses:
      200:
        description: Login bem-sucedido
        schema:
          type: object
          properties:
            token:
              type: string
              description: Token JWT para autenticação
      401:
        description: Credenciais inválidas
      400:
        description: Entrada inválida
      405:
        description: Método não permitido
      500:
        description: Erro interno do servidor
    """
    try:
        if request.method != 'POST':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = service.get_user_by_email(email)
        if user and cripto.check_password(password, user.password):
            claims = {"email": user.email, "name": user.username}
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims=claims,
                expires_delta=timedelta(hours=1)
            )
            return jsonify({"token": access_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@userprints.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Deleta um usuário pelo ID
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT no formato "Bearer {token}"
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser deletado
    responses:
      200:
        description: Usuário deletado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User deleted successfully"
      404:
        description: Usuário não encontrado
      401:
        description: Não autorizado - token inválido ou ausente
      405:
        description: Método não permitido
      500:
        description: Erro interno do servidor
    """
    try:
        if request.method != 'DELETE':
            return jsonify({"error": "Method not allowed"}), 405
        
        result = service.delete_user(user_id)
        if result:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@userprints.route('/update/<int:user_id>', methods=['PUT'])  
@jwt_required()
def update_user(user_id):
    """
    Atualiza os dados de um usuário
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token JWT no formato "Bearer {token}"
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser atualizado
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Novo nome de usuário
            email:
              type: string
              format: email
              description: Novo e-mail do usuário
            password:
              type: string
              format: password
              description: Nova senha do usuário
            is_active:
              type: boolean
              description: Status de ativação do usuário
    responses:
      200:
        description: Usuário atualizado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User updated successfully"
      400:
        description: Entrada inválida
      401:
        description: Não autorizado - token inválido ou ausente
      404:
        description: Usuário não encontrado
      405:
        description: Método não permitido
      500:
        description: Erro interno do servidor
    """
    try:
        if request.method != 'PUT':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data = request.get_json()
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            is_active=data.get('is_active'),
            password=cripto.hash_password(data.get('password'))
        )
        
        updated_user = service.update_user(user_id, user)
        if updated_user is None:
            return jsonify({"message": "User not found"}), 404       
        
        return jsonify({"message": "User updated successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500