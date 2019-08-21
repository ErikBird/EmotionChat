# Create tables for all models
from run import db
from EmoChatApp.models import *
db.create_all()