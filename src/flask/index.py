import pprint
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


def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/registration', methods=['GET','POST'])
def registration():
    if session.get('logged_in'):
        return 'ALREADY LOGGED IN!'
    if request.method == 'POST':
        init_db();
        db=connect_db();
        cur=db.execute('select * from users where username=?',[request.form['username']])
        entries = cur.fetchall()
        if len(entries) is 0:
            db.execute('insert into users (username,password) values(?,?)',[request.form['username'], request.form['password']])
            return pprint.pformat(entries)
        else:
            return 'Username taken'
    else:
        return render_template('registration.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        return 'Verify'
    else:
        return render_template('login.html')

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
