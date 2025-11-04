from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy() # Defines database object
DB_NAME = "main_database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'French' # Used to verify that session data is consistent.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Database path
    db.init_app(app)

    from .views import views
    from .auth import auth 
    # Registering the blueprints I created in the views and auth folders...
    app.register_blueprint(views, url_prefix='/user')
    app.register_blueprint(auth, url_prefix='/auth')

    from . import models # Fetches all models from models.py

    with app.app_context():
        db.create_all()

    return app

# def create_db(app): # Prevents redundant databases/tables from being created.
#     if not path.exists('app/' + DB_NAME): # Checks whether the database exists in the current folder.
#         db.create_all(app=app)
#         print("Creation success.")
#     else:
#         print("The database was not created.")

