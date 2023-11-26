from app import app
from flask_sqlalchemy import SQLAlchemy

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