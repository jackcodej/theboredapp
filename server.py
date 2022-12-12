"""Server for theboredapp"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db

# Better logging from jinja2 using the StrictUndefined class
from jinja2 import StrictUndefined

#Set a variable named 'app' to a new flask server reference server.py
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Flask decorator to denote the home page, and run the homepage function
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')




# Python3, only run the lines if server.py is ran directly
if __name__ == "__main__":
    connect_to_db(app)
    #Set app to run on debug mode at localhost ip address, and run the app
    app.run(host="0.0.0.0", debug=True)