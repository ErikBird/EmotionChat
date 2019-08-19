from flask import Flask,Response, url_for,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
#from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__,root_path='EmotionChat')

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@db'

if Config.ENV == "PRODUCTION":
    app.config.from_object('instance.config.ProductionConfig')
elif Config.ENV == "DEVELOPMENT":
    app.config.from_object('instance.config.DevelopmentConfig')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager = LoginManager()
login_manager.init_app(app)


socketio = SocketIO(app)
from EmotionChat.views import *

if __name__ == "__main__":
    socketio.run(app ,host ="0.0.0.0", port ='5000')

    #app.run(host="0.0.0.0", use_reloader=False)

