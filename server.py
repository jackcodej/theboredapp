"""Server for theboredapp"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db
import crud

# Better logging from jinja2 using the StrictUndefined class
from jinja2 import StrictUndefined

#Set a variable named 'app' to a new flask server reference server.py
app = Flask(__name__)
# Needed to push app's context due to context error when 
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Flask decorator to denote the home page, and run the homepage function
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


# Creates account but not preventing duplicates
@app.route('/create-account', methods=["POST"])
def create_account():
    """Create an account."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    zip_code = request.form.get("zipcode")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with provided email. Please try again")
    else:
        user = crud.create_user(name=name, email=email, password=password, zip_code=zip_code)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return render_template('homepage.html')


# Incomplete
@app.route('/sign-in', methods=["POST"])
def sign_in():
    """Sign in."""

    return render_template('homepage.html')


# Python3, only run the lines if server.py is ran directly
if __name__ == "__main__":
    connect_to_db(app)
    #Set app to run on debug mode at localhost ip address, and run the app
    app.run(host="0.0.0.0", debug=True)