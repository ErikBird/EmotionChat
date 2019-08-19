from run import app,db
from flask import Flask,Response, url_for,request,render_template,redirect,flash,jsonify
from flask_login import current_user, login_user,logout_user,login_required
from run import login_manager
from EmotionChat.models import User
from EmotionChat.forms import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(mail=form.email.data).all():
            flash('E-Mail already taken')
        elif db.session.query(User).filter_by(username=form.username.data).all():
            flash('Username already taken')
        else:
            new_user = User(username=form.username.data, mail=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has beed created')
            login_user(new_user, remember=False)
            return redirect(url_for('chat'))
    return render_template('signup.html', form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            return '<h1> User not found!</h1>'
        if not user.check_password(form.password.data):
            return '<h1> Wrong Password!</h1>'
        login_user(user, remember=form.remember.data)
        flash('You are now logged in')
        return redirect(url_for('chat'))
    return render_template('login.html', form=form)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

@app.route('/about')
def about():
    return 'The about page'
