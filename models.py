from app import db
from sqlalchemy import event

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    high_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Veritabanı indeksleri
event.listen(User.username, 'set', lambda target, value, oldvalue, initiator:
            value.lower() if value else value)