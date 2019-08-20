from run import app,db
from flask import Flask,Response, url_for,request,render_template,redirect,flash,jsonify
from flask_login import current_user, login_user,logout_user,login_required
from run import login_manager,socketio,sentiment_model
from EmotionChat.models import User
from EmotionChat.forms import *
from flask_socketio import send,emit
import operator

active_user = {} #Dict keeps track of all available user for Socket IO


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@socketio.on('connect', namespace='/chat')
def on_connect():
    '''
    Method confirms a Socket connection
    :return:
    '''
    print('Connect: ', request.sid)
    '''
    if request.sid not in server_variables.keys():
        server_variables[request.sid] = {'sid': request.sid, 'stats': 'connected'}
        print("Client connected %s" % request.sid )
        # to broadcaset to all but self
        for k in server_variables.keys():
            if k != request.sid:
                emit('my response', {'data': 'This sid ' + str(request.sid) + ' just connected', 'stats': 'RUNNING'}, room=k)
        # to send only to first socket that was connected to this server
        #emit('my response', {'data': 'This sid ' + str(request.sid) + ' just connected', 'stats': 'RUNNING'},
        #     room=server_variables[server_variables.keys()[0]]['sid'])
    '''

@socketio.on('userdata', namespace='/chat')
def update_user(user):
    '''
    Method gets triggered by the connection event
    It updates the Dictionary with the Username and the Socket ID
    We can directly communicate with this ID
    :param user: new connected user
    :return:
    '''
    active_user[user['data']]=(request.sid,'ACTIVE')
    [print(user) for user in active_user.keys()]


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    '''
    Gets triggered when a Socket gets disconnected
    It deletes the Entry in the dictionary.
    :return:
    '''
    for key, val in active_user.items():
        if val[0] == request.sid: active_user[key]=(request.sid, 'INACTIVE')
    print( str(request.sid) + '=> Client Disconnected ')



@app.route('/')
def index():
    '''
    Startpage
    :return:
    '''
    return render_template('index.html')


@socketio.on('massage', namespace='/chat')
def handle_message(payLoad):
    '''
    This method distributes a message to a given Target.
    The message is furthermore annotated with sentimental information:
    :param payLoad: Message text and the target username
    :return:
    '''
    recipient_session_id = active_user[payLoad['username']][0]
    print('Message: '+payLoad['text'])
    message = payLoad['text']

    emoji_mapping = {
        'neg':':(',
        'pos':':)',
        'neu':':|',
    }
    sentiment_dist = sentiment_model.polarity_scores(message)
    sentiment_dist = dict((k, sentiment_dist[k]) for k in ('neg', 'pos', 'neu')) #Remove the Compond Score
    sentiment=max(sentiment_dist.items(), key=operator.itemgetter(1))[0]
    message = message+' '+emoji_mapping.get(sentiment, ":S")

    emit('new_message',message, room=recipient_session_id )
    emit('new_message', message, room=request.sid)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Method to register a user. The Method ensure exclusivity for the E-Mail and Username
    :return:
    '''
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
    '''
    Login a user.
    :return:
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if not user:
            flash('User not found!')
        if not user.check_password(form.password.data):
            flash('Wrong Password!')
        login_user(user, remember=form.remember.data)
        flash('You are now logged in')
        return redirect(url_for('index_chat'))
    return render_template('login.html', form=form)


@app.route('/chat/<username>', methods=['GET', 'POST'])
def user_chat(username):
    '''

    :param username:
    :return:
    '''
    user = request.form.getlist('handles[]')
    if not user:
        user = active_user.keys()
    return render_template("chat.html", user = user , receiver=username)


@app.route('/chat',)
@login_required
def index_chat():
    user = request.form.getlist('handles[]')
    if not user:
        user = active_user.keys()
    return render_template('chat_base.html', user = user)

@app.route('/logout')
@login_required
def logout():
    '''Logout a User'''
    logout_user()
    return 'You are now logged out!'

@app.route('/about')
def about():
    '''
    To be done.
    :return:
    '''
    return 'The about page'

