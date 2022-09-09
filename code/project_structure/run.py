# from the app package import the app variable(inside __init__.py)
from app import app

# checks if file is executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
