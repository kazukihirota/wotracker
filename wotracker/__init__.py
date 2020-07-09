# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session, render_template, flash
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from passlib.hash import pbkdf2_sha256
import os
from datetime import timedelta
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from .wtform_fields import *

# decorator for routes that should be accessible only by logged in users
from .auth_decorator import login_required

# App config
db=SQLAlchemy()

app = Flask(__name__)

#Configure flask login
login_manager = LoginManager(app)

def create_app():
    app.debug=True

    # Session config
    # app.secret_key = os.environ.get('SECRET_KEY')
    app.secret_key = 'thisismysecretkey'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=50)

    #database 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rfshrwhoqqqxem:b84b85bd8e3068de7363634fbf0137ae36f926cf0ca3f60c78cfc3a02229a5f3@ec2-54-91-178-234.compute-1.amazonaws.com:5432/ddttf394d684r8'
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    #initialise database
    db.init_app(app)
    login_manager.init_app(app)

    #flask bootstrap
    bootstrap = Bootstrap(app)

    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    return app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/howtouse')
def howtouse():
  return render_template('howtouse.html')

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
  return render_template("500.html")

