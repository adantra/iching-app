from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    consultations = db.relationship('Consultation', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    hexagram_data = db.Column(db.Text, nullable=False) # JSON string of raw values
    interpretation = db.Column(db.Text)
    notes = db.Column(db.Text)
    situation = db.Column(db.Text)
    assessment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consultation {self.id}: {self.question}>'

    def set_hexagram_data(self, data):
        self.hexagram_data = json.dumps(data)

    def get_hexagram_data(self):
        return json.loads(self.hexagram_data)
