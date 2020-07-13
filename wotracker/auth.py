from flask import Blueprint, flash, render_template, request, redirect, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .wtform_fields import *
from passlib.hash import pbkdf2_sha256
from .models import User, db
from . import login_manager

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    reg_form = RegistrationForm()
    
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        #Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('auth.login'))

    return render_template("registration.html", form = reg_form)

@auth.route("/login", methods=['GET', 'POST']) 
def login():
    login_form =LoginForm()

    #allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        session.permanent = True
        return redirect(url_for('main.home', username=current_user.username))

    return render_template("login.html", form=login_form)


#verifying if the user is logged in 
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(int(user_id))
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
