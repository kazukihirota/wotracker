from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Optional
from passlib.hash import pbkdf2_sha256

# from .views import exercise_choices
from .models import *

#check if the password matches user
#you can reuse it if you write this function ouside of loginform
def invalid_credentials(form,field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")

#User account registration
class RegistrationForm(FlaskForm):
    
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("User name already exist. select different username")

#Login form
class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')

#Category registration
class CategoryRegForm(FlaskForm):
    category_name = StringField('category_name_label', validators=[InputRequired(message="Name required")])
    submit_button = SubmitField('Add Category')

    def validate_category(self, category_name):
        category_object = Category.query.filter_by(name=category_name.data, userid=current_user.id).first()
        if category_object:
            raise ValidationError("Category already exist.")

#daily record form class and method
def part_choices():
    userid = current_user.id
    qry_part = Category.query.filter(Category.userid==userid).all()
    return qry_part

#Registration form for menu
class ExerciseRegForm(FlaskForm):
    exercise_name = StringField('exercise_name_label', validators=[InputRequired(message="Name required")])
    exercise_part = QuerySelectField('exercise_part_label', query_factory = part_choices, get_label = 'name', allow_blank = False)
    exercise_weight = FloatField('exercise_weight_label', validators=[Optional()])
    exercise_rep = IntegerField('exercise_rep_label', validators=[Optional()])
    exercise_sets = IntegerField('exercise_sets_label', validators=[Optional()])
    submit_button = SubmitField('Add training menu')

class DailyRecordForm(FlaskForm):
    today_part = QuerySelectField('today_part_label', query_factory = part_choices, get_label = 'name', allow_blank = False)
    submit_button = SubmitField('Select the menus')

def exercise_choices():
    return Exercise.query.filter(Exercise.user_id==current_user.id).all()

class DailyExerciseForm(FlaskForm):
    today_exercise = QuerySelectField('today_exercise_label', query_factory = exercise_choices, allow_blank=False, get_label='name')
    today_weight = FloatField('exercise_weight_label', validators=[Optional()])
    today_rep = IntegerField('exercise_rep_label', validators=[Optional()])
    today_sets = IntegerField('today_sets_label', validators=[Optional()])
    submit_button = SubmitField('Add daily training')
