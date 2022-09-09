from flask import Flask, render_template
# import SQLAlchemy(ORM) class from flask_sqlalchemy package
from flask_sqlalchemy import SQLAlchemy

# create app instance
app = Flask(__name__)
# database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# database instance
db = SQLAlchemy(app) # pass-in the app instance as argument

# User model(child class) from parent model(class db.model)
class User(db.Model):
    # primary key(automatically generated)
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # relationship between models
    # (relationship_to, this model, allows flask to grap all data at one shot)
    eggs = db.relationship('Eggs', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'<{self.username}::{self.id}>'

class Eggs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number_of_eggs = db.Column(db.Integer(), nullable=False, default=0)
    #
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<eggs: {self.number_of_eggs}>'
