import random
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, g, redirect, flash, url_for
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from forms.forms import registration, loginForm, createAccount
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError




app = Flask(__name__, template_folder='static/frontend/public/')
bcrypt = Bcrypt(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
UPLOAD_FOLDER = 'static/frontend/public/profilePhotos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg'])

@app.before_request
def before_request():
        g.username = None
        if 'username' in session:
                g.username = session['username']


@app.route("/dashboard")
def dashboard():        
        if g.username:
                
                return render_template('dashboard.html', username=g.username)
        else:
                flash('Please Login to continue')
                return redirect('Login')



@app.route('/LogIn/', methods=['GET', 'POST'])
def LogIn():
        form = loginForm(request.form)       
        if request.method == 'POST':  
                conn = sqlite3.connect('userData.db')
                
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
                                return render_template('login.html', form=form)                                 
                return render_template("login.html", form=form)        
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():        
        session['logged_in'] = True
        session.clear()
        flash("You have successfully logged out.")
        return redirect('LogIn')

@app.route("/dashboard/Post")
def post():        
        return redirect('dashboard')
        
@app.route("/profile")
def profile():      
        if g.username:  
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()

                c.execute('SELECT * FROM accountData WHERE username LIKE (?)', (g.username, ))
                results = c.fetchall()   
                if results:
                        for row in results:
                                username = row[0]
                                bio = row[3]
                                img_url = 'static/' +row[4]
                                interests = row[5]
                                return render_template("profile.html", bio=bio, img_url=img_url, interests=interests, username=g.username)
        else:
                flash('Please Login to continue')
                return redirect('Login')



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
                        flash((registerForm.username.data) + " Successfully Registered!")
                        session['logged_in'] = True
                        session['username'] = (registerForm.username.data)
                        return redirect('account')                                
                return render_template("signup.html", form=registerForm)
        return render_template('signup.html', form=registerForm)

@app.route('/account', methods=['GET', 'POST'])
def addAccount():
        if g.username:         
                createAccountFrom = createAccount(request.form)   

                if request.method == 'POST':
                        conn =sqlite3.connect('userData.db')
                        print ("Opened database successfully")
                        bio =(createAccountFrom.bio.data)
                        f = request.files.get('upload')
                        imageName = (createAccountFrom.imageName.data)
                        filename = secure_filename(f.filename)
                        filetype = filename.split('.')
                        uploadFile = imageName + ('.') + filetype[1]
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'], uploadFile))
                        interests = "Art"
                        f = request.files.get('photo')
                        entry = [(bio, 'frontend/public/profilePhotos/'+ imageName + '.' + filetype[1], interests, g.username)]
                        with conn:
                                c =conn.cursor()
                                c.execute('SELECT * FROM accountData WHERE username LIKE (?)', (g.username, ))
                                results = c.fetchall()
                                try:
                                        sql = ('''UPDATE accountData SET bio=?, imageName=?, interests=? WHERE username =?''')
                                        c.executemany(sql, entry)
                                        message = "You have updated " + g.username + "'s profile."
                                        flash(message)
                                        return redirect('dashboard')
                                except Exception as e: print(e)
                                
                        return render_template("createAccount.html", form=createAccountFrom)
                else:
                        return render_template('createAccount.html', form=createAccountFrom)
        else:
                flash('Please create an account to continue')
                return redirect('signup')
        



if __name__ == '__main__':
      app.run('localhost', 5000, debug=True)