from . import db
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model, UserMixin): # UserMixin helps with user authentication.
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True) # ID as primary key
    email = db.Column(db.String(100), unique=True) # Email must be unique.
    password = db.Column(db.String(100))

    exercises = db.relationship('Exercises', back_populates='user', cascade='all, delete') # Relationship between Users and Exercises tables.
    # Gives this table access to the exercises table. 
    # Cascade deletes all exercises associated with a user if the user is deleted.
    # Represents a one-to-many relationship.


class Exercises(db.Model):
    __tablename__ = 'exercises'


    exercise_id = db.Column(db.Integer, primary_key=True) # Primary key here
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE" )) # Foreign key to link to the Users table.
    # CASCADE will delete all exercises associated with a user if the user is deleted.

    question_data = db.Column(db.JSON) # JSON field to store question data.
    correct = db.Column(db.Integer) # Number of correct answers.
    incorrect = db.Column(db.Integer) # Number of incorrect answers.
    totalQuestions = db.Column(db.Integer) # Total number of questions.
    timeElapsed = db.Column(db.Integer) # Time taken to complete the exercise, in seconds

    timestamp = db.Column(db.DateTime, default=datetime.now()) # Timestamp of when the exercise was completed.

    user = db.relationship('Users', back_populates='exercises', cascade='all, delete')
    # Basically tells that each exercise belongs to a user.
    # Makes user's details available based on the exercise data, vice versa.


