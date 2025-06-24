from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from Backend.resources import sc
from flask_migrate import Migrate
from Backend.extensions import db, jwt  # Import from extensions.py
import os

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": [
    "http://localhost:8080",   # Frontend on the same machine
    "http://10.244.53.76:8080" # Frontend on another device in the network
]}})
    # CORS(app)

    # Configure database
    instance_path = os.path.abspath(os.path.join(app.root_path, 'instance'))
    os.makedirs(instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "app.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Import namespaces AFTER initializing extensions
    from .api.auth import api as auth_ns

    authorizations = {
        "jsonwebtoken": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
    
    api = Api(app, authorizations=authorizations, security='jsonwebtoken')
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(sc)  # Register your medicine reminder endpoints here
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Do NOT use db.create_all() if using Flask-Migrate!
        pass
    app.run(debug=True)