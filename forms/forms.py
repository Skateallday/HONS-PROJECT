from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    FileField, TextField, validators, RadioField, SelectMultipleField
from wtforms.widgets import TextArea
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_components import DateTimeField, DateRange
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from flask import session
from wtforms.validators import NumberRange

class MultiCheckboxField(SelectMultipleField):
	widget			= ListWidget(prefix_label=False)
	option_widget	= CheckboxInput()

class loginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('login')

class registration(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class createAccount(FlaskForm):
    bio = StringField('bio', widget=TextArea())
    interests = SelectField('interests', choices=[('Art', 'Art'), ('Music', 'Music'), ('Sports', 'Sports'), ('Travel', 'Travel'),('Food', 'Food'), ('Gaming', 'Gaming'), ('Film', 'Film'), ('Politics', 'Politics')])
    upload = FileField('Upload Profile Image',validators=[FileRequired()])
    imageName = StringField('imageName', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Finish Creating Account!')

class postStatus(FlaskForm):
    postTitle = StringField('title', validators=[DataRequired(), Length(min=2, max=50)])
    postContent = StringField('content', validators=[DataRequired()], widget=TextArea())
    category = SelectField('category', choices=[('Art', 'Art'), ('Music', 'Music'), ('Sports', 'Sports'), ('Travel', 'Travel'),('Food', 'Food'), ('Gaming', 'Gaming'), ('Film', 'Film'), ('Politics', 'Politics')])
    upload = FileField('Upload Profile Image')
    submit = SubmitField('Send it!')

