from . import db
from flask_login import UserMixin

class Users(db.Model, UserMixin): # UserMixin helps with user authentication.
    id = db.Column(db.Integer, primary_key=True) # ID as primary key
    email = db.Column(db.String(100), unique=True) # Email must be unique.
    password = db.Column(db.String(100))


