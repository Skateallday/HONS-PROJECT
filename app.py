import random
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, g, redirect, flash, url_for
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from forms.forms import registration, loginForm, createAccount, postStatus, createGroup, postComment
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import datetime

app = Flask(__name__, template_folder='static/frontend/public/templates')
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

@app.route('/aboutUs')
def aboutUs():
        return render_template('aboutUs.html')

@app.route("/dashboard")
def dashboard():        
        if g.username:
                form = postStatus(request.form)  
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()
                c.execute('SELECT author, imageName, postTitle, postContent, category, dateTime FROM accountData INNER JOIN userPost ON userPost.author = accountData.username ORDER BY dateTime DESC');  
                posts = c.fetchall()
                print(posts) 
                for post in posts:
                        author = post[0]
                        imageName = [1]
                        postTitle = post[2]
                        postContent = post[3]
                        category = post[4]
                        if request.method == 'POST':
                                conn = sqlite3.connect('userData.db')
                                print ("User Posts data opened")
                                c = conn.cursor()
                                newPost = [(g.username, (form.postTitle.data), (form.postContent.data), (form.category.data))]
                                with conn:
                                        try:
                                                insertPost = '''INSERT INTO userPost (username, postTitle, postContent, category) VALUES(?,?,?,?)'''
                                                c.executemany(insertPost, newPost)
                                                print ("Insert correctly")
                                        except Exception as e: print(e)                                                        
                                        flash((g.username) + " Successfully Posted!!")
                                        return render_template("profile.html", form=form, postTitle=postTitle, postContent=postContent, category=category)                                        
                return render_template('dashboard.html', posts=posts, username=g.username)
        else:
                flash('Please Login to continue')
                return redirect('Login')

@app.route("/groups", methods=['GET', 'POST'])
def groups():        
        if g.username:
                form = createGroup(request.form)  
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()
                c.execute('SELECT * FROM groups');  
                groups = c.fetchall()
                print(groups)    
                if request.method == 'POST':
                                conn = sqlite3.connect('userData.db')
                                print ("Group data opened")
                                c = conn.cursor()
                                groupImage = "public/groupImages/" + form.groupName.data + '.jpg'
                                newGroup = [((form.groupName.data), (form.groupBio.data), (form.groupType.data), g.username, '150', (groupImage))]
                                with conn:
                                        try:
                                                insertPost = '''INSERT INTO groups (groupName, groupBio, groupType, groupMembers, groupSize, groupImage) VALUES(?,?,?,?,?,?)'''
                                                c.executemany(insertPost, newGroup)
                                                print ("Insert correctly")
                                        except Exception as e: print(e)                                                        
                                        flash((g.username) + " Successfully Posted!!")   
                                return render_template('groups.html', groupImage=groupImage, form=form, groups=groups, username=g.username)                                               
                return render_template('groups.html', form=form, groups=groups, username=g.username)
        else:
                flash('Please Login to continue')
                return redirect('Login')

@app.route("/subgroup/id/<subgroup>", methods=['GET', 'POST'])
def subgroup(subgroup):    
        subgroup=subgroup
        if g.username:
                form = postComment(request.form)  
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()
                findgroup = ('SELECT * FROM groups WHERE groupId LIKE ?') 
                c.execute(findgroup, subgroup)
                groups = c.fetchall()
                loadComments = ('SELECT * FROM groupComments WHERE groupId LIKE ?')
                c.execute(loadComments, subgroup)
                comments = c.fetchall()
                print(groups)    
                if request.method == 'POST':
                                conn = sqlite3.connect('userData.db')
                                print ("Group data opened")
                                c = conn.cursor()
                                comment = [(subgroup, g.username, (form.comment.data), '0' )]
                                with conn:
                                        try:
                                                insertPost = '''INSERT INTO groupComments (groupId, author, comment, votes, dateTime) VALUES(?,?,?,?, datetime('now', 'localtime'))'''
                                                c.executemany(insertPost, comment)
                                                print ("Insert correctly")
                                        except Exception as e: print(e)                                                        
                                        flash((g.username) + " Successfully Posted!!")   
                                return render_template('subgroups.html', subgroup=subgroup,  form=form, comments=comments, groups=groups, username=g.username)                                               
                return render_template('subgroups.html', subgroup=subgroup, form=form, comments=comments, groups=groups, username=g.username)
        else:
                flash('Please Login to continue')
                return redirect('Login')

@app.route("/cheer/id/<commentId>")
def cheer(commentId):
        if g.username:
                commentId=commentId        
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()
                checkVotes = ('SELECT dailyVotes FROM accountData WHERE username LIKE ?')
                c.execute(checkVotes, [g.username])
                votesChecked = c.fetchone()
                if int(votesChecked[0]) >= 0:
                        findgroup = ('SELECT * FROM groupComments WHERE commentId LIKE ?') 
                        c.execute(findgroup, commentId)
                        cheer = c.fetchall()
                        for cheers in cheer:
                                with conn:
                                        try:
                                                c = conn.cursor()
                                                changeCheers = '''UPDATE  groupComments SET votes = votes + 1 WHERE commentID = ?'''
                                                c.execute(changeCheers, commentId)
                                                updateDailyVotes = '''UPDATE accountData SET dailyVotes = dailyVotes - 1 WHERE username = ?'''
                                                c.execute(updateDailyVotes, [g.username])
                                                print ("Insert correctly")
                                        except Exception as e:print(e)

                        return redirect('subgroup/id/'+str(cheers[1]))
                else: 
                        findgroup = ('SELECT groupId FROM groupComments WHERE commentId LIKE ?') 
                        c.execute(findgroup, commentId)
                        groupId = c.fetchone()
                        flash('You have no more votes left for today!')
                        return redirect('subgroup/id/'+str(int(groupId[0])))
        else:
                flash('Please Login to continue')
                return redirect('Login')



@app.route("/boo/id/<commentId>")
def boo(commentId):        
        if g.username:
                commentId=commentId        
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()
                checkVotes = ('SELECT dailyVotes FROM accountData WHERE username LIKE ?')
                c.execute(checkVotes, [g.username])
                votesChecked = c.fetchone()
                if int(votesChecked[0]) >= 0:
                        findgroup = ('SELECT * FROM groupComments WHERE commentId LIKE ?') 
                        c.execute(findgroup, commentId)
                        cheer = c.fetchall()
                        for cheers in cheer:
                                with conn:
                                        try:
                                                c = conn.cursor()
                                                changeCheers = '''UPDATE  groupComments SET votes = votes - 1 WHERE commentID = ?'''
                                                c.execute(changeCheers, commentId)
                                                updateDailyVotes = '''UPDATE accountData SET dailyVotes = dailyVotes - 1 WHERE username = ?'''
                                                c.execute(updateDailyVotes, [g.username])
                                                print ("Insert correctly")
                                        except Exception as e:print(e)

                        return redirect('subgroup/id/'+str(cheers[1]))
                else: 
                        findgroup = ('SELECT groupId FROM groupComments WHERE commentId LIKE ?') 
                        c.execute(findgroup, commentId)
                        groupId = c.fetchone()
                        flash('You have no more votes left for today!')
                        return redirect('subgroup/id/'+str(int(groupId[0])))
        else:
                flash('Please Login to continue')
                return redirect('Login')
       


@app.route('/Login/', methods=['GET', 'POST'])
def LogIn():
        form = loginForm(request.form)       
        if request.method == 'POST':  
                conn = sqlite3.connect('userData.db')                
                with conn:
                        c = conn.cursor()
                        find_user = ("SELECT * FROM accountData WHERE username = ?")
                        c.execute(find_user, [(form.username.data)])  
                        results =c.fetchall()
                        
                        userResults = results[0]
                        if bcrypt.check_password_hash(userResults[2],(form.password.data)):
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
        return redirect('Login')

@app.route("/dashboard/Post")
def post():        
        return redirect('dashboard')
        
@app.route("/profile", methods=['GET', 'POST'])
def profile():      
        if g.username:
                form = postStatus(request.form)  
                conn =sqlite3.connect('userData.db')
                print ("Opened database successfully")
                c = conn.cursor()

                c.execute('SELECT * FROM accountData WHERE username LIKE (?)', (g.username, ))
                results = c.fetchall()
                c.execute('SELECT * FROM userPost WHERE author LIKE(?) ORDER BY dateTime DESC', (g.username, ))  
                posts = c.fetchall()
                print(results) 
                if results:
                        for row in results:
                                username = row[0]
                                bio = row[3]
                                img_url = 'static/' +row[4]
                                interests = row[5]                                
                                if posts:
                                        for post in posts:
                                                postTitle = post[1]
                                                postContent = post[2]
                                                category = post[3]
                                                return render_template("profile.html", form=form, postTitle=postTitle, postContent=postContent, category=category, bio=bio, img_url=img_url, interests=interests, username=g.username)
                                else:
                                        if request.method == 'POST':
                                                        conn = sqlite3.connect('userData.db')
                                                        print ("User Posts data opened")
                                                        c = conn.cursor()
                                                        newPost = [(g.username, (form.postTitle.data), (form.postContent.data), (form.category.data))]
                                                        with conn:
                                                                try:
                                                                        insertPost = '''INSERT INTO userPost (author, postTitle, postContent, category, dateTime) VALUES(?,?,?,?, datetime('now', 'localtime'))'''
                                                                        c.executemany(insertPost, newPost)
                                                                        print ("Insert correctly")
                                                                except Exception as e: print(e)                                                        
                                                                flash((g.username) + " Successfully Posted!!")
                        return render_template("profile.html", bio=bio, img_url=img_url, interests=interests, form=form, username=g.username)                
                
        else:
                flash('Please Login to continue')
                return redirect('Login')


@app.route("/profile/user/<user>", methods=['GET', 'POST'])
def profileUserName(user):      
        user = user

        form = postStatus(request.form) 
        conn =sqlite3.connect('userData.db')
        print ("Opened database successfully")
        c = conn.cursor()
        c.execute('SELECT * FROM accountData WHERE username LIKE (?)', (user, ))
        results = c.fetchall()
        c.execute('SELECT * FROM userPost WHERE author LIKE(?)', (user, ))  
        posts = c.fetchall()
        print(results) 
        print(posts)
        if request.method == 'POST':
                conn = sqlite3.connect('userData.db')
                print ("User Posts data opened")
                c = conn.cursor()
                newPost = [(g.username, (form.postTitle.data), (form.postContent.data), (form.category.data))]
                with conn:
                        try:
                                insertPost = '''INSERT INTO userPost (author, postTitle, postContent, category, dateTime) VALUES(?,?,?,?, datetime('now', 'localtime'))'''
                                c.executemany(insertPost, newPost)
                                print ("Insert correctly")
                        except Exception as e: print(e)                                                        
                        flash((g.username) + " Successfully Posted!!")
        else: 
                if results:
                        for row in results:
                                username = row[0]
                                bio = row[3]
                                img_url = '../../static/' +row[4]
                                interests = row[5]                                
                                if posts:
                                        for post in posts:
                                                postTitle = post[1]
                                                postContent = post[2]
                                                category = post[3]                                                
                                                return render_template("profile.html", form=form, postTitle=postTitle, postContent=postContent, category=category, bio=bio, img_url=img_url, interests=interests, username=user)
                                else:
                                        return render_template("profile.html", bio=bio, img_url=img_url, interests=interests, form=form, username=user)
                else:
                        return redirect(404)              
                


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
        if g.username:
                return redirect('dashboard')
        else:
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
        

@app.errorhandler(404)
def page_not_found(e):        
        return render_template('404.html'), 404

if __name__ == '__main__':
      app.run('localhost', 5000, debug=True)