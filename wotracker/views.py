from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from flask_login import logout_user, current_user, login_required
from datetime import datetime
from .models import *
from .wtform_fields import *

bp = Blueprint('main', __name__)

@bp.route('/<username>/home')
@login_required
def home(username):
    user=User.query.filter_by(username=username).first()
    categories = Category.query.order_by(Category.id).all()
    return render_template('home.html', user=user, categories = categories)

@bp.route('/<username>/menulog/<int:categoryid>/')
def menulog(categoryid, username):
    user=User.query.filter_by(username=username).first()
    categories = Category.query.filter(Category.id==categoryid)
    exercises = Exercise.query.filter(Exercise.category_id == categoryid, Exercise.user_id == user.id)
    return render_template('menulog.html', exercises = exercises, categories = categories)

@bp.route('/menureg', methods=['GET', 'POST'])
@login_required
def menureg():
    exercise_form = ExerciseRegForm()

    if exercise_form.validate_on_submit():
        name = exercise_form.exercise_name.data
        part = exercise_form.exercise_part.data
        weight = exercise_form.exercise_weight.data
        rep = exercise_form.exercise_rep.data
        sets= exercise_form.exercise_sets.data
        user_id = current_user.id

        exercise = Exercise(name=name, category_id = part, weight = weight, rep = rep, sets = sets, user_id = user_id)
        db.session.add(exercise)
        db.session.commit()

        flash('Your exercise successfully added!','success')

        return redirect(url_for('main.menureg'))

    return render_template('menureg.html', form = exercise_form)

@bp.route('/dailyrecord', methods=['GET', 'POST'])
@login_required
def dailyrecord():
    daily_record_form = DailyRecordForm()
    if daily_record_form.validate_on_submit():
        
    return render_template('dailyrecord.html')


@bp.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('index'))