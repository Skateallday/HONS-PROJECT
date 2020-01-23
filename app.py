import random
import os
import sqlite3
from flask import Flask, render_template, request, session, g, redirect, flash, url_for
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from forms.forms import registration, loginForm
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


@app.route("/dashboard")
def dashboard():        
        if g.username:
                
                return render_template('dashboard.html')
        else:
                flash('Please Login to continue')
                return redirect('Login')



@app.route('/', methods=['GET', 'POST'])
@app.route('/LogIn/', methods=['GET', 'POST'])
def LogIn():
        form = loginForm(request.form)       
        if request.method == 'POST':  
                conn = sqlite3.connect('loginData.db')
                
                with conn:
                        c = conn.cursor()
                        find_user = ("SELECT * FROM loginDetails WHERE username = ?")
                        c.execute(find_user, [(form.username.data)])  
                        results =c.fetchall()
                        
                        userResults = results[0]
                        if bcrypt.check_password_hash(userResults[1],(form.password.data)):
                                session['logged_in'] = True
                                session['username'] = (form.username.data)
                                return redirect(url_for('dashboard'))
                        else:
                                flash('Either username or password was not recognised')
                                return render_template('index.html', form=form) 

                                 
                return render_template("index.html", form=form)
        
        return render_template("index.html", form=form)

@app.route("/logout")
def logout():        
        session['logged_in'] = True
        session.clear()
        flash("You have successfully logged out.")
        return redirect('home')


@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    registerForm = registration(request.form)   

    if request.method == 'POST':
            pw_hash =bcrypt.generate_password_hash(registerForm.password.data)
            newEntry = [((registerForm.username.data), pw_hash, (registerForm.emailAddress.data))]
            conn =sqlite3.connect('loginData.db')
            print ("Opened database successfully")
            with conn:
                    c =conn.cursor()
                    try:
                            sql = '''INSERT INTO loginDetails (username, password, email) VALUES(?,?,?)'''
                            c.executemany(sql, newEntry)
                            print ("Insert correctly")
                    except:
                            flash("This is already an account, please log in with those details or change details.")
                            return render_template("signup.html", form=registerForm)
                            c.commit()

                    flash((registerForm.username.data) + " Successfully Registered!")
                    return redirect('LogIn')
            return render_template("signup.html", form=registerForm)

    return render_template('signup.html', form=registerForm)


if __name__ == '__main__':
      app.run('localhost', 5000, debug=True)