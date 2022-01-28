# Here a Flask instance is created inside a function known as the application factory
# This file also tells python that the Website directory should be treated as a package

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path

# define a new database 
db = SQLAlchemy()

# assign database name 
DB_NAME = 'database.db'

# create application factory
def create_app():
    # create flask application object
    app = Flask(__name__) # name is the current python module
    
    app.config['SECRET_KEY'] = 'dev' # secure web app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #SQL database stored at sqlite:/// (in the website folder)
    db.init_app(app) # defines the app being used with the database

    from .views import views # import blueprints for the routes/views

    app.register_blueprint(views, url_prefix='/') # register blueprints & state how they are accessed on the app 
        # we want all prefixes to be / as it goes before the prefix defined on blueprint
    
    from .models import Location, SNP # check we have loaded the models.py file

    create_database(app)

    return app # create Flask app


def create_database(app): # check if database already exists & if not create it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
