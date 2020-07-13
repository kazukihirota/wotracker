# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session, render_template, flash
from authlib.integrations.flask_client import OAuth

from .extensions import db, login_manager
from flask_bootstrap import Bootstrap

from .wtform_fields import *

# decorator for routes that should be accessible only by logged in users
from .auth_decorator import login_required

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    #initialise database
    db.init_app(app)

    #initialise login manager
    login_manager.init_app(app)

    #flask bootstrap
    bootstrap = Bootstrap(app)

    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.auth)

    return app