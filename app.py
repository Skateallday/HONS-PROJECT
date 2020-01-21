import random
import os
import sqlite3
from flask import Flask, render_template, request, session, g, redirect, flash, url_for
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from forms.forms import registration, logon
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError



app = Flask(__name__, template_folder='static/frontend/public/')
bcrypt = Bcrypt(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

@app.before_request
def before_request():
        g.username = None
        if 'username' in session:
                g.username = session['username']

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = registration(request.form)   

    if request.method == 'POST':
            pw_hash =bcrypt.generate_password_hash(registerForm.password.data)
            newEntry = [((registerForm.username.data), pw_hash, (registerForm.emailAddress.data))]
            conn =sqlite3.connect('testData.db')
            print ("Opened database successfully")
            with conn:
                    c =conn.cursor()
                    try:
                            sql = '''INSERT INTO users (username, password, email) VALUES(?,?,?)'''
                            c.executemany(sql, newEntry)
                            print ("Insert correctly")
                    except:
                            flash("This is already an account, please log in with those details or change details.")
                            return render_template("register.html", form=registerForm)
                            c.commit()

                    flash((registerForm.username.data) + " Successfully Registered!")
                    return redirect('login')
            return render_template("register.html", form=registerForm)

    return render_template('signup.html', form=registerForm)


if __name__ == '__main__':
      app.run('localhost', 5000, debug=True)