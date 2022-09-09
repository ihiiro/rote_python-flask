from flask import Flask, render_template

app = Flask(__name__)

# set URL as function-call URL
@app.route('/')
@app.route('/main') # this is also function call URL
# said function
def main_page():
    return 'main-page'

# another route
@app.route('/non-main')
def non_main():
    return 'non-main'

# dynamic URL
@app.route('/profile/<username>') # <username> is a URL-variable
def profile(username): # pass URL-variable as parameter to function
    return f'Welcome {username}! to your profile.'

# return templates
@app.route('/html')
def main_page_html():
    numbers = [
        {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    ]
    # argument #1: filename, argument #2: data
    return render_template('home.html', username="ducky", numbers=numbers)
