from datetime import datetime
from extensions import db 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    profile_picture = db.Column(db.String(200))
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    medicines = db.relationship('UserMedMap', backref='user', lazy=True)
    health_entries = db.relationship('DailyHealthEntry', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Fixed relationship
    user_med_maps = db.relationship('UserMedMap', backref='medicine', lazy=True)

class UserMedMap(db.Model):
    __tablename__ = 'user_med_map'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    breakfast_before = db.Column(db.Boolean, default=False)
    breakfast_after = db.Column(db.Boolean, default=False)
    lunch_before = db.Column(db.Boolean, default=False)
    lunch_after = db.Column(db.Boolean, default=False)
    dinner_before = db.Column(db.Boolean, default=False)
    dinner_after = db.Column(db.Boolean, default=False)
    
    # Fixed relationships (remove duplicate back_populates)
    statuses = db.relationship('Status', backref='med_map', lazy=True)

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_med_map_id = db.Column(db.Integer, db.ForeignKey('user_med_map.id'), nullable=False)
    is_taken = db.Column(db.Boolean, default=False)

class DailyHealthEntry(db.Model):
    __tablename__ = 'daily_health_entry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    bp_systolic = db.Column(db.Float)
    bp_diastolic = db.Column(db.Float)
    sugar_level = db.Column(db.Float)
