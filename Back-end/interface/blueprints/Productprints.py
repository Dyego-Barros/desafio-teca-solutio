from flask import Blueprint, request, jsonify
from domain.entities.ProductEntity import ProductEntity as Product
from application.services.ProductService import ProductService
from flask_jwt_extended import jwt_required

productprint = Blueprint('productprint', __name__)

service = ProductService()

@productprint.route('/create', methods=['POST'])
@jwt_required()
def create_prdutc():
    try:
        if request.method != 'POST':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data  = request.get_json()
        product = Product(
            nome=data.get('nome'),
            marca=data.get('marca'),
            valor=data.get('valor'),
            in_stock=data.get('in_stock'),
            
        )
        #Deve publicar numa fila redis para ser consumido pelo serviço
        service.create_product(product) 
        
        return jsonify({"message": "Criação de produto enfileirado com sucesso"}), 200
        
        
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@productprint.route('/list', methods=['GET'])
@jwt_required()
def list_products():
    try:
        products = service.get_all_products()
        if products is None:
            return jsonify({"message": "No products found"}), 404
        
        products_list = [{k:v for k,v in vars(product).items() if k  != '_sa_instance_state'}
                         for product in products]
        print(products_list)
        return jsonify(products_list), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@productprint.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        if request.method != 'PUT':
            return jsonify({"error": "Method not allowed"}), 405
        
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data  = request.get_json()
        product = Product(
            nome=data.get('nome'),
            marca=data.get('marca'),
            valor=data.get('valor'),           
            in_stock=data.get('in_stock'),
        )
        
        updated_product = service.update_product(product_id, product)
        if updated_product is None:
            return jsonify({"message": "Produto não encontrado"}), 404       
        
        return jsonify({"message": "Atualizaça2o de produto enfileirada com sucesso!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@productprint.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        if request.method != 'DELETE':
            return jsonify({"error": "Method not allowed"}), 405
        
        result = service.delete_product(product_id)
        if result is False:
            return jsonify({"message": "Produto não encontrado"}), 404
        
        return jsonify({"message": "Deleção de produto enfileirada com sucesso!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500