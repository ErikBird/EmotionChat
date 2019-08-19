from run import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128))
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    def check_password(self, password):
        return check_password_hash(self.password, password)