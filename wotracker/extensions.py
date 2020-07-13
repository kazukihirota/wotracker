from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# App config
db=SQLAlchemy()

#Configure flask login
login_manager = LoginManager()