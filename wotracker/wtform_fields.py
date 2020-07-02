from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from .models import User

#check if the password mathes user
#you can reuse it if you write this function ouside of loginform
def invalid_credentials(form,field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("User name already exist. select different username")

class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')

class ExerciseRegForm(FlaskForm):
    exercise_name = StringField('exercise_name_label', validators=[InputRequired(message="Name required")])
    exercise_part = SelectField('exercise_part_field', choices=[('1','shoulder'),('2','chest'), ('3','back'), ('4','arm'),('5', 'leg'),('6','others')])
    exercise_weight = FloatField('exercise_weight_label')
    exercise_rep = IntegerField('exercise_rep_label')
    exercise_sets = IntegerField('exercise_sets_label')
    submit_button = SubmitField('Add Training Menu')

class DailyRecordForm(FlaskForm):
    today_part = Selectfield('today_part_label', choices=[('1','shoulder'),('2','chest'), ('3','back'), ('4','arm'),('5', 'leg'),('6','others')])
    today_exercise = 
