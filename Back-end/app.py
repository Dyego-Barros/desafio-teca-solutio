from flask import Flask
from core.database.Database import Engine, Session, Base
from interface.blueprints.Productprints import productprint
from interface.blueprints.Userprints import userprints
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
#Secret key para sessões
app.config['SECRET_KEY'] =  os.environ.get("SECRET_KEY")
# Chave secreta para JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  

# Configuração do Swagger
app.config['SWAGGER'] = {
    'title': 'User API',
    'uiversion': 3,
    'description': 'API para gerenciamento de usuários com autenticação JWT',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token JWT no formato: Bearer {token}'
        }
    },
    'security': [{'Bearer': []}]
}

swagger = Swagger(app)

# Inicializar JWTManager 
jwt = JWTManager(app)

#Registra rotas
app.register_blueprint(productprint, url_prefix='/product')
app.register_blueprint(userprints, url_prefix='/user')



Base.metadata.create_all(Engine)
Session()

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)   
