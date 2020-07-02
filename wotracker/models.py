from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64),nullable=False)
    exercises = db.relationship('Exercise', backref='Category', cascade="all, delete-orphan")

class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64),nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    weight = db.Column(db.Float)
    rep = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  