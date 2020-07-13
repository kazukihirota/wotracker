from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from flask_login import logout_user, current_user, login_required
from datetime import datetime
from .models import *
from .wtform_fields import *

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/howtouse')
def howtouse():
  return render_template('howtouse.html')

@bp.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("404.html")

@bp.errorhandler(500)
def internal_error(e):
  return render_template("500.html")


@bp.route('/<username>/home')
@login_required
#user specific
def home(username):
    user=User.query.filter_by(username=username).first()
    categories = Category.query.filter(Category.userid==user.id).all()
    dailyrecords = DailyRecord.query.filter(DailyRecord.user_id==current_user.id).order_by(DailyRecord.date.desc()).limit(10).all()
    dailyexercises = DailyExercise.query.all()
    return render_template('home.html', user=user, categories = categories, dailyrecords = dailyrecords, dailyexercises = dailyexercises)

#see the menus for a specific part 
@bp.route('/<username>/menulog/<int:categoryid>/')
#user specific
def menulog(categoryid, username):
    user=User.query.filter_by(username=username).first()
    categories = Category.query.filter(Category.id==categoryid)
    exercises = Exercise.query.filter(Exercise.category_id == categoryid, Exercise.user_id == user.id)
    return render_template('menulog.html', exercises = exercises, categories = categories)

#see all the menus 
@bp.route('/<username>/allmenus')
def allmenulog(username):
    user=User.query.filter_by(username=username).first()
    categories = Category.query.filter(Category.userid==current_user.id).all()
    exercises = Exercise.query.filter(Exercise.user_id == user.id).all()

    return render_template('allmenulog.html', exercises = exercises, categories = categories)

@bp.route('/<username>/alldailyrecords')
def alldailyrecord(username):
    dailyrecords = DailyRecord.query.filter(DailyRecord.user_id==current_user.id).order_by(DailyRecord.date.desc()).all()
    dailyexercises = DailyExercise.query.all()

    return render_template('alldailyrecord.html', dailyrecords = dailyrecords, dailyexercises = dailyexercises)



###### Addition #########



#add new category (training part)
@bp.route('/categoryreg', methods=['GET', 'POST'])
@login_required
def categoryreg():
    category_form = CategoryRegForm()

    if category_form.validate_on_submit():
        name = category_form.category_name.data
        userid = current_user.id

        category = Category(name=name, userid=userid)
        db.session.add(category)
        db.session.commit()

        flash('Your category successfully added!', 'success')

        return redirect(url_for('main.categoryreg'))

    return render_template('categoryreg.html', form = category_form) 

#Add new menu to the database
@bp.route('/menureg', methods=['GET', 'POST'])
@login_required
def menureg():
    exercise_form = ExerciseRegForm()

    if exercise_form.validate_on_submit():
        name = exercise_form.exercise_name.data
        part = exercise_form.exercise_part.data.id #get id from category!!!!
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

#adding menu from daily record 
@bp.route('/menuregindaily', methods=['GET', 'POST'])
@login_required
def menuregindaily():
    exercise_form = ExerciseRegForm()

    if exercise_form.validate_on_submit():
        name = exercise_form.exercise_name.data
        part = exercise_form.exercise_part.data.id #get id from category!!!!
        weight = exercise_form.exercise_weight.data
        rep = exercise_form.exercise_rep.data
        sets= exercise_form.exercise_sets.data
        user_id = current_user.id

        category = exercise_form.exercise_part.data.name

        exercise = Exercise(name=name, category_id = part, weight = weight, rep = rep, sets = sets, user_id = user_id)
        db.session.add(exercise)
        db.session.commit()

        flash('successfully added','success')

        return redirect(url_for('main.dailyexercises', category=category))

    return render_template('menuregindaily.html', form = exercise_form)


#Adding daily record
@bp.route('/dailyrecord', methods=['GET', 'POST'])
@login_required
def dailyrecord():
    
    daily_record_form = DailyRecordForm()
    todays_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    #get all the category today for the user
    categories_exist = DailyRecord.query.filter(DailyRecord.user_id==current_user.id, DailyRecord.date==todays_date).all()

    if daily_record_form.validate_on_submit():
        dt = todays_date
        categoryname = daily_record_form.today_part.data.name
        user_id = current_user.id

        if not categories_exist: #making new daily record for the day 
           
            dailyrecord = DailyRecord(date = dt, category = categoryname, user_id = user_id)
            db.session.add(dailyrecord)
            db.session.commit()

            return redirect(url_for('main.dailyexercises', category=categoryname))

        else:
            #there is at least one daily record
            for category_exist in categories_exist:
                if categoryname == category_exist.category:
                    category = categoryname

                    return redirect(url_for('main.dailyexercises', category = categoryname))
                
            dailyrecord = DailyRecord(date = dt, category = categoryname, user_id = user_id)
            db.session.add(dailyrecord)
            db.session.commit()

            return redirect(url_for('main.dailyexercises', category = categoryname))

    return render_template('dailyrecord.html', form = daily_record_form)


#Register exercises in daily record
@bp.route('/dailyexercises/<category>', methods=['GET', 'POST'])
@login_required
def dailyexercises(category):
    daily_exercise_form = DailyExerciseForm()

    userid=current_user.id
    todays_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

    #exercise part 
    part = DailyRecord.query.filter(DailyRecord.user_id==userid, DailyRecord.date==todays_date, DailyRecord.category==category).first()

    #querying choices 
    categoryid = Category.query.filter_by(name=category).first().id
    daily_exercise_form.today_exercise.query = Exercise.query.filter(Exercise.category_id==categoryid).all()

    if daily_exercise_form.validate_on_submit():
        
        dailyrecordid = DailyRecord.query.filter(DailyRecord.user_id==userid, DailyRecord.date==todays_date, DailyRecord.category==category).first().id
        exercise = daily_exercise_form.today_exercise.data.name
        weight = daily_exercise_form.today_weight.data
        rep = daily_exercise_form.today_rep.data
        sets = daily_exercise_form.today_sets.data

        dailyexercise = DailyExercise(dailyrecord_id = dailyrecordid, exercise = exercise, weight = weight, rep = rep, sets = sets)
        db.session.add(dailyexercise)
        db.session.commit()

        flash('Successfully added', 'success')

        return redirect(url_for('main.dailyexercises', category=category))

    return render_template('dailyexercise.html', form = daily_exercise_form, part=part)

# def exercise_choices(categoryid):
#     userid = current_user.id
#     qry = Exercise.query.filter(Exercise.user_id==userid, Exercise.category_id==categoryid).all()
#     return qry

##### Deletion #####

#Delete category
@bp.route('/deletecategory/<int:id>', methods=['POST'])
@login_required
def deletecategory(id):

    #delete category itself
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)

    #delete all the exercises in the category
    exercises = Exercise.query.filter(Exercise.category_id==id).all()
    for exercise in exercises:
        db.session.delete(exercise)

    db.session.commit()

    flash('the exercise successfully deleted', 'success')

    return redirect(url_for('main.allmenulog', username=current_user.username))

#Delete menu
@bp.route('/deletemenu/<int:id>', methods=['POST'])
@login_required
def deletemenu(id):
    menu = Exercise.query.filter_by(id=id).first()
    name = Exercise.query.filter_by(id=id).first().name
    dailyexercise = DailyExercise.query.filter(DailyExercise.exercise==name).all()

    #delete from menu
    db.session.delete(menu)

    #delete from daily records
    for exercise in dailyexercise:
        db.session.delete(exercise)

    db.session.commit()

    flash('the exercise successfully deleted', 'success')

    return redirect(url_for('main.allmenulog', username=current_user.username))

#Delete daily exercise from daily record
@bp.route('/deletedailyexercise/<int:id>', methods=['POST'])
@login_required
def deletedailyexercise(id):
    dailyexercise = DailyExercise.query.filter_by(id=id).first()
    recordid = dailyexercise.dailyrecord_id

    #querying all exercises in the same daily record id
    otherdailyexercises = DailyExercise.query.filter(DailyExercise.dailyrecord_id==recordid).all() 
    dailyrecordtodelete = DailyRecord.query.filter(DailyRecord.id==recordid).first()

    #delete exercise record from the daily record
    db.session.delete(dailyexercise)

    #if there is no other exercises, delete daily record itself
    if not otherdailyexercises:
        db.session.delete(dailyrecordtodelete)

    db.session.commit()

    flash('The exercise record is successfully deleted','success')

    return redirect(url_for('main.alldailyrecord', username=current_user.username))

#Delete daily record itself
@bp.route('/deletedailyrecord/<int:id>', methods=['POST'])
@login_required
def deletedailyrecord(id):
    dailyrecord = DailyRecord.query.filter_by(id=id).first()
    dailyexercises = DailyExercise.query.filter(DailyExercise.dailyrecord_id==id).all()

    db.session.delete(dailyrecord)

    if dailyexercises is not None:
        for dailyexercise in dailyexercises:
            db.session.delete(dailyexercise)

    db.session.commit()

    flash('the exercise record is successfully deleted','success')

    return redirect(url_for('main.alldailyrecord', username=current_user.username))

#logout
@bp.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('index'))