import builtins
from collections import OrderedDict
import csv
from datetime import date, timedelta, datetime
from functools import wraps
import io
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import pandas as pd
from flask import request, jsonify
from flask_restx import Resource, Namespace, reqparse, marshal, fields
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required, get_jwt, verify_jwt_in_request
from sqlalchemy import distinct, exists, func, null,extract
from sqlalchemy.orm import aliased, joinedload, subqueryload, contains_eager
import logging

from Backend.models import *
# from .api_models import *
# from .helper import *

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

assign_medicine_model = sc.model('AssignMedicine', {
    'medicine_id': fields.Integer(required=True),
    'dosage': fields.Integer(required=True),
    'start_date': fields.String(required=True, description='YYYY-MM-DD'),
    'end_date': fields.String(required=True, description='YYYY-MM-DD'),
    'breakfast_before': fields.Boolean(required=False, default=False),
    'breakfast_after': fields.Boolean(required=False, default=False),
    'lunch_before': fields.Boolean(required=False, default=False),
    'lunch_after': fields.Boolean(required=False, default=False),
    'dinner_before': fields.Boolean(required=False, default=False),
    'dinner_after': fields.Boolean(required=False, default=False),
    'had_taken' : fields.Boolean(required=False, default=False),
    'random' : fields.Boolean(required=False, default=False),
})

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

@sc.route("/assign-medicine", methods=["POST"])
class AssignMedicine(Resource):
    @jwt_required()
    @sc.expect(assign_medicine_model, validate=True)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        try:
            assignment = UserMedMap(
                user_id=user_id,
                medicine_id=data["medicine_id"],
                dosage=data["dosage"],
                start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
                breakfast_before=data.get("breakfast_before", False),
                breakfast_after=data.get("breakfast_after", False),
                lunch_before=data.get("lunch_before", False),
                lunch_after=data.get("lunch_after", False),
                dinner_before=data.get("dinner_before", False),
                dinner_after=data.get("dinner_after", False),
                had_taken=data.get("had_taken", False)
            )
            db.session.add(assignment)
            db.session.flush() 
            start_date = assignment.start_date.date()
            end_date = assignment.end_date.date()
            delta = (end_date - start_date).days + 1
            for i in range(delta):
                current_date = start_date + timedelta(days=i)
                status = Status(
                    user_med_map_id=assignment.id,
                    date=current_date,
                    breakfast_before=False if assignment.breakfast_before else None,
                    breakfast_after=False if assignment.breakfast_after else None,
                    lunch_before=False if assignment.lunch_before else None,
                    lunch_after=False if assignment.lunch_after else None,
                    dinner_before=False if assignment.dinner_before else None,
                    dinner_after=False if assignment.dinner_after else None
                )
                db.session.add(status)
            db.session.commit()
            return {"message": "Medicine assigned and status tracking initialized."}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


@sc.route("/unassign-medicine/<int:medicine_id>",methods=["DELETE"])
class UnassignMedicine(Resource):
    @jwt_required()
    def delete(self, medicine_id):
        user_id=get_jwt_identity()
        assignment=UserMedMap.query.filter_by(user_id=user_id, medicine_id=medicine_id).first()
        if not assignment:
                return {"error": "Assignment not found."}, 404
        try:
            db.session.delete(assignment)
            db.session.commit()
            return {"message": "Medicine unassigned successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

@sc.route("/medicine-status/<int:medicine_id>", methods=["GET"])
class MedicineStatus(Resource):
    @jwt_required()
    def get(self, medicine_id):
        user_id = get_jwt_identity()
        date_str = request.args.get('date')
        if not date_str:
            return {"error": "Date is required in 'YYYY-MM-DD' format as a query parameter."}, 400
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}, 400
        user_med_map = UserMedMap.query.filter_by(user_id=user_id, medicine_id=medicine_id).first()
        if not user_med_map:
            return {"error": "Medicine assignment not found."}, 404
        status = Status.query.filter_by(user_med_map_id=user_med_map.id, date=target_date).first()
        if not status:
            return {"error": "No status entry found for this date."}, 404
        return {
            "medicine_id": medicine_id,
            "date": target_date.isoformat(),
            "statuses": {
                "breakfast_before": status.breakfast_before,
                "breakfast_after": status.breakfast_after,
                "lunch_before": status.lunch_before,
                "lunch_after": status.lunch_after,
                "dinner_before": status.dinner_before,
                "dinner_after": status.dinner_after
            }
        }, 200

@sc.route("/status-report", methods=["GET"])
class StatusReport(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)
        if not month or not year:
            return {"error": "Month and year are required."}, 400
            
        # Get all status entries for the user for that month and year
        statuses = db.session.query(Status).join(UserMedMap).filter(
            UserMedMap.user_id == user_id,
            extract('month', Status.date) == month,
            extract('year', Status.date) == year
        ).all()
        
        result = {}
        for status in statuses:
            date_str = status.date.strftime('%Y-%m-%d')
            slot_statuses = {
                "breakfast_before": status.breakfast_before,
                "breakfast_after": status.breakfast_after,
                "lunch_before": status.lunch_before,
                "lunch_after": status.lunch_after,
                "dinner_before": status.dinner_before,
                "dinner_after": status.dinner_after
            }
            taken = sum(1 for v in slot_statuses.values() if v is True)
            missed = sum(1 for v in slot_statuses.values() if v is False)
            result[date_str] = {
                "taken": taken,
                "missed": missed,
                "details": slot_statuses 
            }
        return result, 200

@sc.route("/api/medicine-reminder", methods=["POST"])
class CreateMedicineReminder(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        user_med_map_id = data.get("user_med_map_id")
        reminder_times = data.get("reminder_times", [])
        notification_type = data.get("notification_type", "push")
        message = data.get("message", "Time to take your medicine.")

        # Validate user_med_map belongs to current user
        user_med_map = UserMedMap.query.filter_by(
            id=user_med_map_id,
            user_id=user_id
        ).first()
        if not user_med_map:
            return {"error": "Assignment not found or not authorized."}, 404

        # Create reminders for each time slot
        for time_slot in reminder_times:
            reminder = MedicineReminder(
                user_med_map_id=user_med_map_id,
                reminder_time=time_slot,
                notification_type=notification_type,
                message=message,
                active=True
            )
            db.session.add(reminder)
        db.session.commit()
        return {"message": "Reminders scheduled successfully."}, 201

@sc.route("/api/medicine-reminder", methods=["GET"])
class GetMedicineReminders(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        reminders = MedicineReminder.query.join(UserMedMap).filter(
            UserMedMap.user_id == user_id,
            MedicineReminder.active == True
        ).all()
        result = []
        for reminder in reminders:
            result.append({
                "reminder_id": reminder.id,
                "medicine_title": reminder.user_med_map.medicine.title,
                "reminder_time": reminder.reminder_time,
                "notification_type": reminder.notification_type,
                "message": reminder.message,
                "active": reminder.active
            })
        return result, 200

@sc.route("/api/medicine-reminder/<int:reminder_id>", methods=["DELETE"])
class DeleteMedicineReminder(Resource):
    @jwt_required()
    def delete(self, reminder_id):
        user_id = get_jwt_identity()
        reminder = MedicineReminder.query.join(UserMedMap).filter(
            MedicineReminder.id == reminder_id,
            UserMedMap.user_id == user_id
        ).first()
        if not reminder:
            return {"error": "Reminder not found or not authorized."}, 404
        reminder.active = False
        db.session.commit()
        return {"message": "Reminder deactivated successfully."}, 200
