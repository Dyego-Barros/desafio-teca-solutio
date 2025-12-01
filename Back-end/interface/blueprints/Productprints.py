from flask import Blueprint, request, jsonify
from domain.entities.ProductEntity import ProductEntity as Product
from application.services.ProductService import ProductService
from flask_jwt_extended import jwt_required
from flasgger.utils import swag_from

productprint = Blueprint('productprint', __name__)
service = ProductService()

@productprint.route('/create', methods=['POST'])
@jwt_required()
@swag_from({
    'security': [{'Bearer': []}],
    'tags': ['Products']
})
def create_product():
    """
    Cria um novo produto (operações são enfileiradas no Redis)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
     
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - marca
            - valor
            - in_stock
          properties:
            nome:
              type: string
              description: Nome do produto
            marca:
              type: string
              description: Marca do produto
            valor:
              type: number
              format: float
              description: Valor do produto
            in_stock:
              type: boolean
              description: Status de disponibilidade em estoque
    responses:
      200:
        description: Criação de produto enfileirada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Criação de produto enfileirado com sucesso"
      400:
        description: Entrada inválida ou JSON mal formatado
      401:
        description: Não autorizado - token inválido ou ausente
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
        product = Product(
            nome=data.get('nome'),
            marca=data.get('marca'),
            valor=data.get('valor'),
            in_stock=data.get('in_stock'),
        )
        # Deve publicar numa fila redis para ser consumido pelo serviço
        service.create_product(product) 
        
        return jsonify({"message": "Criação de produto enfileirado com sucesso"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@productprint.route('/list', methods=['GET'])
@jwt_required()
def list_products():
    """
    Lista todos os produtos cadastrados
    ---
    tags:
      - Products
    security:
      - Bearer: []  
    responses:
      200:
        description: Lista de produtos retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID do produto
              nome:
                type: string
                description: Nome do produto
              marca:
                type: string
                description: Marca do produto
              valor:
                type: number
                format: float
                description: Valor do produto
              in_stock:
                type: boolean
                description: Status de disponibilidade em estoque
      404:
        description: Nenhum produto encontrado
      401:
        description: Não autorizado - token inválido ou ausente
      500:
        description: Erro interno do servidor
    """
    try:
        products = service.get_all_products()
        if products is None:
            return jsonify({"message": "No products found"}), 404
        
        products_list = [{k:v for k,v in vars(product).items() if k != '_sa_instance_state'}
                         for product in products]
        
        return jsonify(products_list), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@productprint.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    Atualiza um produto existente (operações são enfileiradas no Redis)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:      
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID do produto a ser atualizado
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Novo nome do produto
            marca:
              type: string
              description: Nova marca do produto
            valor:
              type: number
              format: float
              description: Novo valor do produto
            in_stock:
              type: boolean
              description: Novo status de disponibilidade em estoque
    responses:
      200:
        description: Atualização de produto enfileirada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Atualização de produto enfileirada com sucesso!"
      400:
        description: Entrada inválida ou JSON mal formatado
      401:
        description: Não autorizado - token inválido ou ausente
      404:
        description: Produto não encontrado
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
        product = Product(
            nome=data.get('nome'),
            marca=data.get('marca'),
            valor=data.get('valor'),           
            in_stock=data.get('in_stock'),
        )
        
        updated_product = service.update_product(product_id, product)
        if updated_product is None:
            return jsonify({"message": "Produto não encontrado"}), 404       
        
        return jsonify({"message": "Atualização de produto enfileirada com sucesso!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@productprint.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    Deleta um produto (operações são enfileiradas no Redis)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:      
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID do produto a ser deletado
    responses:
      200:
        description: Deleção de produto enfileirada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Deleção de produto enfileirada com sucesso!"
      401:
        description: Não autorizado - token inválido ou ausente
      404:
        description: Produto não encontrado
      405:
        description: Método não permitido
      500:
        description: Erro interno do servidor
    """
    try:
        if request.method != 'DELETE':
            return jsonify({"error": "Method not allowed"}), 405
        
        result = service.delete_product(product_id)
        if result is False:
            return jsonify({"message": "Produto não encontrado"}), 404
        
        return jsonify({"message": "Deleção de produto enfileirada com sucesso!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500