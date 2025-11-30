from flask import Flask
from core.database.Database import Engine, Session, Base
from interface.blueprints.Productprints import productprint
from interface.blueprints.Userprints import userprints
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] =  os.environ.get("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  # Chave secreta para JWT
# Inicializar JWTManager corretamente
jwt = JWTManager(app)


app.register_blueprint(productprint, url_prefix='/product')
app.register_blueprint(userprints, url_prefix='/user')



Base.metadata.create_all(Engine)
Session()

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)   
