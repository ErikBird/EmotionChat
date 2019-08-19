from flask import Flask,Response, url_for,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
from flask_apscheduler import APScheduler
#from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__,root_path='EmotionChat')

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@db'

if Config.ENV == "PRODUCTION":
    app.config.from_object('instance.config.ProductionConfig')
elif Config.ENV == "DEVELOPMENT":
    app.config.from_object('instance.config.DevelopmentConfig')

db = SQLAlchemy(app)
scheduler = APScheduler()
login_manager = LoginManager()
scheduler.init_app(app)
login_manager.login_view = "login"
scheduler.start()
login_manager = LoginManager()
login_manager.init_app(app)



#from EmotionChat.models import *
#migrate = Migrate(app, db)

from EmotionChat.views import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=False)

