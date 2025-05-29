from flask import Flask
from flask_restx import Api
from extensions import db, jwt  # Import from extensions.py
import os

def create_app():
    app = Flask(__name__)
    
    # Configure database
    instance_path = os.path.abspath(os.path.join(app.root_path, 'instance'))
    os.makedirs(instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "app.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    # Import namespaces AFTER initializing extensions
    from api.auth import api as auth_ns
    
    api = Api(app)
    api.add_namespace(auth_ns, path='/auth')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables within app context
    app.run(debug=True)
