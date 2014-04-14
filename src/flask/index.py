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

@app.route('/debug')
def debug():
    #init_db()
    db = get_db()
    cur=db.execute('select * from users')
    entries = cur.fetchall()
    ret = ''
    for user in entries:
        ret+=user['username']
        ret += "\n"
    return ret
#    return pprint.pformat(entries)

@app.route('/')
def welcome_page():
    return render_template('home.html')

@app.route('/registration', methods=['GET','POST'])
def registration():
    if session.get('logged_in'):
        return redirect(url_for('notes'))
    if request.method != 'POST':
       return redirect(url_for('welcome_page'))
  
    db=connect_db();
    cur=db.execute('select * from users where username=?',[request.form['username']])
    entries = cur.fetchall()
    if len(entries) is 0:
        error = db.execute('insert into users (username,password,email) values(?,?,?)',[request.form['username'], request.form['password'], request.form['email']])
        db.commit()
        if (len(error.fetchall()) is 0):
            flash('Account created')
            redirect(url_for('login'))
        else:
            flash('Account could not be created')
            return render_template('home.html', error='Account could not be created!')
    else:
        return render_template('home.html',error='Username taken')
@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('notes'))
    if request.method == 'POST':
        error = None
        db=get_db();
        cur=db.execute('select * from users where username=? and password=?',[request.form['username'],request.form['password']])
        entries = cur.fetchall()
        if len(entries) is 0:
            flash('Invalid username/password combination')
            return render_template('login.html')
        else:
            session['logged_in']=True
            flash('Logged in successfully')
            return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('Logged out successfully')
    return render_template('index.html')

@app.route('/notes/new', methods=['POST'])
def newNotes():
    return 1
@app.route('/notes/edit', methods=['POST'])
def editNotes():
    return 1

@app.route('/notes/delete', methods=['POST'])
def deleteNotes():
    return 1

@app.route('/notes')
def notes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db=get_db();
    cur=db.execute('select * from notes')
    entries = cur.fetchall()
    return render_template('notes.html', notes=entries)


def connect_db():
#    rv = sqlite3.connect('/var/www/flaskr.db')
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory=sqlite3.Row
    return rv

def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

if __name__ == '__main__':
    app.run(debug=True)
