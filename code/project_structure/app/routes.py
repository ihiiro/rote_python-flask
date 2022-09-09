from app import app
from flask import render_template
from app.models import Product

@app.route('/')
def main():
    products = Product.query.all()
    return render_template('main.html', products=products)
