from flask import Flask,Response, url_for,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
#from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_session import Session
import nltk
import os

STATIC_DIR = os.path.abspath('./EmoChatApp/static')
app = Flask(__name__,root_path='EmoChatApp' , static_folder=STATIC_DIR)
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager = LoginManager()
login_manager.init_app(app)

#Manage Sessions by the explicit Server-Side Sessions to get a coherent syncroisation btw. the server and the websocket sessions
Session(app)
socketio = SocketIO(app , manage_session=False) #Manage Session False to be able to access the Flask Sessions

if Config.ENV == "PRODUCTION":
    app.config.from_object('instance.config.ProductionConfig')
else:
    app.config.from_object('instance.config.DevelopmentConfig')


#Sentiment Model
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment_model = SentimentIntensityAnalyzer()



from EmoChatApp.views import *

if __name__ == "__main__":
    socketio.run(app ,host ="0.0.0.0", port ='5000')
