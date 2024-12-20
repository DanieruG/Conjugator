from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session # Message handling, page switching.
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def authenticate(): # Handles the login process.
    if request.method == "POST": # If request method is POST, then receive the fields
        email_field = request.form.get('emailField') # Gets data sent by AJAX
        pass_field = request.form.get('passField')

        user = Users.query.filter_by(email=email_field).first() # First instance of the email.
        if user and check_password_hash(user.password, pass_field):
            user_id = user.id
            session['id'] = user_id
            session['email'] = email_field
            return "Login success. Redirecting to dashboard in 5s.", 200 # You will need to flash this, to then redirect the user.
        else:
            return "Invalid login. Please check your details and try again.", 401
    
    return render_template("login.html")
           
@auth.route('/register', methods=["GET", "POST"])
def upload_details(): # Uploads the user's details to the database.
    success = False # Flag to monitor whether details have been added or not.
    if request.method == "POST": # If request method is POST, then receive the fields
        email_field = request.form.get('emailField') # Gets data sent by AJAX
        pass_field = request.form.get('passField')

        new_user = Users(email=email_field, password=generate_password_hash(pass_field, method="pbkdf2:sha256"))
        try:
            db.session.add(new_user) # Adds a new user to the database
            db.session.commit() # Saves this change
            success = True
        except IntegrityError: # In the case that the email already exists.
            db.session.rollback() # Undoes changes
            success = False
        
        if success:
            return "Registration was successful. You will be redirected to the login page.", 200
        else:
            return "This email already exists. Please try a different email.", 400

    return render_template('register.html')


