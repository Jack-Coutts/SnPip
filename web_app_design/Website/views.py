# here the standard routes for the web app will be stored

from flask import Blueprint, render_template 

# here we will define that this file is a blueprint of the application
# it has routes that you can find in it (some URLs)
views = Blueprint('views', __name__) # set up a blueprint for the Flask app

# define a route or view
@views.route('/') # this is the home page
def home(): # this function will run whenever we go to this route
    return render_template('home.html') # Home page template

@views.route('/about') # this is the about page
def about(): # this function will run whenever we go to this route
    return render_template('about.html')

@views.route('/documentation') # this is the documentation page
def documentation(): # this function will run whenever we go to this route
    return render_template('documentation.html')

@views.route('/search') # this is the search page
def search(): # this function will run whenever we go to this route
    return render_template('search.html')
