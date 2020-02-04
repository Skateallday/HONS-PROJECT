import random
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, g, redirect, flash, url_for
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from forms.forms import registration, loginForm, createAccount, postStatus
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import datetime

app = Flask(__name__, template_folder='static/frontend/public/')
bcrypt = Bcrypt(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
UPLOAD_FOLDER = 'static/frontend/public/profilePhotos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg'])

@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
        registerForm = registration(request.form) 
        if request.method == 'POST':
                pw_hash =bcrypt.generate_password_hash(registerForm.password.data)
                newEntry = [((registerForm.username.data), pw_hash, (registerForm.emailAddress.data), ' ', 'frontend/public/profilePhotos/placeholder.jpg', '' )]

                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                with conn:
                        c =conn.cursor()
                        try:
                                signupSQL = '''INSERT INTO accountData (username, password, email, bio, imageName, interests) VALUES(?,?,?,?,?,?)'''
                                c.executemany(signupSQL, newEntry)
                                print ("Insert correctly")
                        except:
                                flash("This is already an account, please log in with those details or change details.")
                                return render_template("signup.html", form=registerForm)
                                c.commit()
                        flash((registerForm.username.data) + " thanks for signing up! We will email you soon with more information once this site is further along the development process!")
                        session['logged_in'] = True
                        session['username'] = (registerForm.username.data)
                        return redirect('signup')                                
                return render_template("signup.html", form=registerForm)
        return render_template('signup.html', form=registerForm)


@app.errorhandler(404)
def page_not_found(e):        
        return render_template('404.html'), 404

if __name__ == '__main__':
      app.run('localhost', 5000, debug=True)