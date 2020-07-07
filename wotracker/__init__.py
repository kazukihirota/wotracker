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
    app.secret_key = os.environ.get('SECRET_KEY')
    # app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=50)

    #database 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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

# # oAuth Setup
# oauth = OAuth(app)
# google = oauth.register(
#     name='google',
#     client_id='267372206641-q54so3gtau60vfctrg6ru1q0s62ffkcg.apps.googleusercontent.com',
#     client_secret='ZbP8Nox-Wl6GK8jX_x8lo9BJ',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  
#     # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
# )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/howtouse')
def howtouse():
  return render_template('howtouse.html')

# #Google login and authorisation
# @app.route('/login_by_google')
# def login_by_google():
#     google = oauth.create_client('google')  # create the google oauth client
#     redirect_uri = url_for('authorize_google', _external=True)
#     return google.authorize_redirect(redirect_uri)

# @app.route('/authorize_google')
# def authorize_google():
#     google = oauth.create_client('google')  # create the google oauth client
#     token = google.authorize_access_token()  # Access token from google (needed to get user info)
#     resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
#     user_info = resp.json()
#     user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
#     # Here you use the profile/user data that you got and query your database find/register the user
#     # and set ur own data in the session not the profile from google
#     session['profile'] = user_info
#     session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
#     return render_template('home.html')

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
  return render_template("500.html")

