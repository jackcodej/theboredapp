"""Server for theboredapp"""

from flask import (Flask, render_template, request, flash, session, redirect, request)

from model import connect_to_db, db
import crud
import requests
import helper

from datetime import date


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


@app.route('/create-account', methods=["POST"])
def create_account():
    """Create an account."""

    # Using jinja to get form inputs from request.form dictionary
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    zip_code = request.form.get("zipcode")

    # Conditional to check if an account with the provided email already exists
    if crud.get_user_by_email(email):
        flash("Cannot create an account with provided email. Please try again.")
    else:
    # Else create a new account
        user = crud.create_user(name=name, email=email, password=password, zip_code=zip_code)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect('/')


@app.route('/sign-in', methods=["POST"])
def sign_in():
    """Sign in."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    # Conditional to check if the user exists and if passwords match
    if not user or user.password != password:
        flash("The provided information was incorrect. Please try again.")
    else:
    # Else store user email in session 
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.name}")

    return redirect("/")


@app.route('/activity/search')
def find_filtered_activity():
    """Query for an activity from boredapi with arguments"""

    url = 'https://www.boredapi.com/api/activity/'

    # Get all values from form **Not request.form because this is not a post request
    # Need to clarify the exact reason why we use request.args.get instead of request.form
    key = request.args.get('key', '')
    a_type = request.args.get('a_type', '')
    participants = request.args.get('participants', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    min_accessibility = request.args.get('min_accessibility', '')
    max_accessibility = request.args.get('max_accessibility', '')

    #TODO: All of these little functions can go into my helper from 93 to 115
    # Conditionals for range values to turn into percentage
    if min_price != '':
        min_price = int(min_price)/100

    if max_price != '':
        max_price = int(max_price)/100

    if min_accessibility != '':
        min_accessibility = int(min_accessibility)/100

    if max_accessibility != '':
        max_accessibility = int(max_accessibility)/100

    # Handle if range of price is not in correct order
    if min_price and max_price and (min_price > max_price):
        temp_min = min_price
        min_price = max_price
        max_price = temp_min
        
    # Handle if range of accessibility is not in correct order
    if min_accessibility and max_accessibility and (min_accessibility > max_accessibility):
        temp_min = min_accessibility
        min_accessibility = max_accessibility
        max_accessibility = temp_min

    payload = {
        'key': key,
        'type': a_type,
        'participants': participants,
        'minprice': min_price,
        'maxprice': max_price,
        'minaccessibility': min_accessibility,
        'maxaccessibility': max_accessibility,
    }

    res = requests.get(url, params=payload)
    data = res.json()

    try:
        # If activity is not already stored in the activity table create a new record
        if not crud.get_activity_by_key(data["key"]):
            activity = crud.create_activity(activity=data["activity"], 
                                                key=data["key"], 
                                                a_type=data["type"], 
                                                link=data["link"], 
                                                price=data["price"], 
                                                participants=data["participants"], 
                                                accessibility=data["accessibility"]
                                                )
            db.session.add(activity)
            db.session.commit()
        else:
            activity = crud.get_activity_by_key(data["key"])
        # If user is signed in create a new record in history
        if "user_id" in session:
            new_history_log = crud.create_history_log(user_id=session["user_id"], 
                                                    activity_id=crud.get_activity_by_key(data["key"]).activity_id, 
                                                    last_clicked=date.today().strftime("%B %d, %Y") #not getting exact time when doing this for some reason
                                                    )
            db.session.add(new_history_log)
            db.session.commit()
        return render_template('activity.html', activity=activity)
    except:
        if data.get('error'):
            flash("This activity doesn't exist :(")
        else:
            flash("An error has occurred, please try again")

        return redirect("/")


@app.route('/activity/history')
def get_activity_by_user():
    """Get the activity history of browser's session user_id"""

    if "user_id" in session:
        user_history = crud.get_user_history(session["user_id"])
    else:
        flash('Please login to your account or register to have access to this feature.')

    return render_template('activity_history.html', user_history=user_history)


# Python3, only run the lines if server.py is ran directly
if __name__ == "__main__":
    connect_to_db(app)
    #Set app to run on debug mode at localhost ip address, and run the app
    app.run(host="0.0.0.0", debug=True)