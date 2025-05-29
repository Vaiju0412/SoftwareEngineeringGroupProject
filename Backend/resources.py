import builtins
from collections import OrderedDict
import csv
from datetime import date
from functools import wraps
import io
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import pandas as pd
from flask import request, jsonify
from flask_restx import Resource, Namespace, reqparse, marshal
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required, get_jwt, verify_jwt_in_request
from sqlalchemy import distinct, exists, func, null
from sqlalchemy.orm import aliased, joinedload, subqueryload, contains_eager
import logging

from .models import *
from .api_models import *
from .helper import *

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Unauthorized

logger = logging.getLogger(__name__)

authorizations = {
    "jsonwebtoken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

sc = Namespace("sc", description="SilverCare Backend API Namespace", authorizations=authorizations)

@sc.route("/api/verify-token")
class VerifyToken(Resource):
    
    def get(self):
        try:
            # Verify the JWT in the request
            verify_jwt_in_request()  # Raises an exception if the token is invalid
            claims = get_jwt()  # Extract claims from the token
            return {
                "valid": True,
                "claims": claims,
                "message": "Token is valid"
            }, 200
        except Unauthorized as e:
            return {
                "valid": False,
                "message": "Invalid or expired token"
            }, 401
        except Exception as e:
            return {
                "valid": False,
                "message": "An error occurred during token verification"
            }, 500

#Edit user
@sc.route('/user/<int:user_id>')
class EditUser(Resource):
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.username = data.get('username', user.username)
        user.role = data.get('role', user.role)
        user.profile_picture = data.get('profile_picture', user.profile_picture)

        # Handling password update
        if 'password' in data:
            user.set_password(data['password'])

        try:
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update user', 'error': str(e)}, 500
        
#Create medicine
@sc.route('/medicine')
class CreateMedicine(Resource):
    @jwt_required()
    def post(self):
        """Create new medicine entry"""
        data = request.get_json()
        user_id = get_jwt_identity()

        medicine = Medicine(
            title=data['title'],
            description=data['description'],
            user_id=user_id,
            image=data.get('image')
        )

        try:
            db.session.add(medicine)
            db.session.commit()
            return {'message': 'Medicine created successfully', 'medicine_id': medicine.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to create medicine', 'error': str(e)}, 500

#Delete medicine
@sc.route('/medicine/<int:medicine_id>')
class DeleteMedicine(Resource):
    @jwt_required()
    def delete(self, medicine_id):
        """Delete a medicine entry by ID."""
        user_id = get_jwt_identity()
        medicine = Medicine.query.filter_by(id=medicine_id, user_id=user_id).first()
        if not medicine:
            return {'message': 'Medicine not found or unauthorized'}, 404

        try:
            db.session.delete(medicine)
            db.session.commit()
            return {'message': 'Medicine deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to delete medicine', 'error': str(e)}, 500

#Edit medicine
@sc.route('/medicine/<int:medicine_id>')
class EditMedicine(Resource):
    @jwt_required()
    def put(self, medicine_id):
        """Update a medicine entry by ID."""
        user_id = get_jwt_identity()
        medicine = Medicine.query.filter_by(id=medicine_id, user_id=user_id).first()
        if not medicine:
            return {'message': 'Medicine not found or unauthorized'}, 404

        data = request.get_json()
        medicine.title = data.get('title', medicine.title)
        medicine.description = data.get('description', medicine.description)
        medicine.image = data.get('image', medicine.image)

        try:
            db.session.commit()
            return {'message': 'Medicine updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update medicine', 'error': str(e)}, 500
