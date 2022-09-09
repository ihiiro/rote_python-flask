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
    name = db.Column(db.String(length=10), nullable=False, unique=True)
    # primary key(automatically generated)
    id = db.Column(db.Integer(), primary_key=True)

    # the way class instances are represented in User.query.all() for example
    def __repr__(self):
        return f'<user:{self.name}>'

@app.route('/')
def hello():
    users = User.query.all()
    return render_template('main.html', users=users)
