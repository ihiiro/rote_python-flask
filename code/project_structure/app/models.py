from app import db

class Product(db.Model):
    name = db.Column(db.String(length=12), nullable=False, unique=True)
    ship_day = db.Column(db.String(length=10), nullable=False)
    id = db.Column(db.Integer(), primary_key=True)
