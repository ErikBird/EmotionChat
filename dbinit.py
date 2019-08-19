# Create tables for all models
from run import db
from EmotionChat.models import *
db.create_all()