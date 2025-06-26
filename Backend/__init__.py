from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from .resources import sc
from .extensions import api, db, jwt
from .models import *

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:8080",
        "http://10.244.53.76:8080"
    ]}})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['JWT_SECRET_KEY'] = 'nsvfdkjgvnkgsmljknjrngovndfmnjnnsjzlkdnvdijoidklnclajrbg'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)
    app.config['SQLALCHEMY_ECHO'] = True

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    api.add_namespace(sc)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return {"id": user.id, "role": user.designation, "z_id": user.username}
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]["id"]
        return User.query.get(identity)

    with app.app_context():
        db.create_all()

    return app
