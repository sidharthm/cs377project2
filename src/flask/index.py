import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
DATABASE=os.path.join(app.root_path,'flaskr.db'),
DEBUG=True,
SECRET_KEY='development key',
USERNAME='admin',
PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS',silent=True);

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
        return 'Verify'
    else:
        return 'Login'

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return 'Logged out'

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory=sqlite3.Row
    return rv

if __name__ == '__main__':
    app.run(debug=True)
