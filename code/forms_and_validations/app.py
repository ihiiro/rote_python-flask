from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# hashing
from flask_bcrypt import Bcrypt
# user authentication imports
from flask_login import (LoginManager, login_user, UserMixin, logout_user,
login_required, current_user)
# flask forms imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# form validation imports(within parathesis cuz it's a long line)
from wtforms.validators import (Length, EqualTo, Email, DataRequired,
ValidationError)





















app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# secret key
app.config['SECRET_KEY'] = '57798ed544580fcb365fa3c7'

db = SQLAlchemy(app)

# create bcrypt instance
bcrypt = Bcrypt(app)

# create LoginManager instance
login_manager = LoginManager(app)

# tell the login_manager the location of the login page
login_manager.login_view = 'login_page'

# set flash message
login_manager.login_message = 'Please login'

# set flash category
login_manager.login_message_category = 'alert'


















# user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f'{self.username}'

    # for password hashing
    @property
    def password(self):
        # password will be stored in this property instead of password_hash
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # then password_hash is going to be set to a hashed version
        # in parathesis because invalid syntax otherwise
        self.password_hash = (bcrypt.generate_password_hash(plain_text_password)
        .decode('utf-8'))

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,
        attempted_password)



























# flask forms(in same file only cuz this is for learning)
class RegisterForm(FlaskForm):
    # render_kw allows to set html element attributes
    username = StringField(label='Username:', validators=
    [Length(min=2, max=30), DataRequired()], render_kw={'autofocus':True})
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),
    DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=
    [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    # prefix all validation functions with validate_
    # and suffix validate_ with fieldname to validate
    def validate_username(self, check_me): # check_me is not good btw
        user = User.query.filter_by(username=check_me.data).first()
        if user:
            raise ValidationError('username already taken!')

    def validate_email(self, check_me):
        user = User.query.filter_by(email=check_me.data).first()
        if user:
            raise ValidationError('email already taken!')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()],
    render_kw={'autofocus':True})
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')






















# routes

# methods argument is required for post requests
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # check if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('forusers'))

    # create form instance
    form = RegisterForm()
    # once the submit button is triggered
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data) # middleman property

        db.session.add(user_to_create)
        db.session.commit()

        # log the user in automatically upon registration
        login_user(user_to_create)
        flash('Account created successfully! You are now logged in',
        category='success')

        return redirect(url_for('forusers'))

    if form.errors != {}: # if the dict is not empty of errors
        for err_msg in form.errors.values():
            flash(f'error: {err_msg[0]}', category='error')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # check if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('forusers'))
        
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = (User.query.filter_by(username=form.username.data)
        .first())
        # if attempted_user is not None
        if attempted_user and attempted_user.check_password_correction(form
        .password.data):
            login_user(attempted_user)
            flash(f'Logged in as: {attempted_user.username}',
            category='success')
            return redirect(url_for('forusers'))
        else:
            flash('wrong username or password!', category='error')

    if form.errors != {}: # if the dict is not empty of errors
        for err_msg in form.errors.values():
            flash(f'error: {err_msg[0]}', category='error')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You logged out!', category='success')

    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forusers')
@login_required
def forusers():
    return render_template('forusers.html')
