from flask import Blueprint, request, jsonify
from domain.entities.UserEntity import UserEntity as User
from application.services.UserService import UserService
from core.helpers.Criptograph import Criptograph
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from flask_restx import Api, Resource, fields

cripto = Criptograph()
service = UserService()

userprints = Blueprint('userprints', __name__)
api = Api(userprints,doc='/docs', title='User API', description='API for user management')

@userprints.route('/create', methods=['POST'])
def create_user():
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
            access_token = create_access_token(identity=str(user.id), additional_claims=claims,expires_delta=timedelta(hours=1))
            return jsonify({"token":access_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 

@userprints.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
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
    try:
        if request.method != 'PUT':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data  = request.get_json()
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
