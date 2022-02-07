# Here a Flask instance is created inside a function known as the application factory
# This file also tells python that the Website directory should be treated as a package

import os
from flask import Flask


# create application factory
def create_app():
    # create flask application object
    app = Flask(__name__) # name is the current python module

    return app # create Flask app



