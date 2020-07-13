import os 
from datetime import timedelta

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
PERMANENT_SESSION_LIFETIME = timedelta(days=50)