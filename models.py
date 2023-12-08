from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app=app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(100), nullable=False)
    register_number = db.Column(db.String(20), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    accomodation = db.Column(db.String(20), nullable=False)
    email_id = db.Column(db.String(120), nullable=False)
    hostel_block = db.Column(db.String(1))
    gender = db.Column(db.String(10), nullable=False)
    checked_in = db.Column(db.Boolean, default = False)
    onboarding_email_sent = db.Column(db.Boolean, default=False, nullable=False)
    slug = db.Column(db.String(100), nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String(200), nullable=False)
    form_details = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(100), nullable=False)

class FormFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_uid = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    form = db.relationship('Form', backref='form_fields')
    question = db.Column(db.String(255), nullable=False)
    input_type = db.Column(db.String(50), nullable=False)

