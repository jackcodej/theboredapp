"""Server for theboredapp"""

from flask import (Flask, render_template, request, flash, session, redirect, request, jsonify)

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


@app.route('/registration')
def show_registration_page():
    """Navigate to registration page."""

    return render_template('registration_sign_in.html', registration=True)

    
@app.route('/login')
def show_login_page():
    """Navigate to login page."""

    return render_template('registration_sign_in.html', registration=False)


@app.route('/logout')
def logout():
    """Log out."""

    # Delete user information from session if currently logged in
    if "user_id" in session:
        del session["user_id"]
    if "user_email" in session:
        del session["user_email"]
        flash(f"You have been logged out successfully!")

    return render_template('logout.html')


@app.route('/registration', methods=["POST"])
def register_account():
    """Register an account."""

    # Using jinja to get form inputs from request.form dictionary
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    zip_code = request.form.get("zipcode")

    # Conditional to check if an account with the provided email already exists
    if crud.get_user_by_email(email) or email == "":
        flash("Cannot create an account with provided email. Please try again.")
        return redirect('/registration')
    else:
    # Else create a new account
        user = crud.create_user(name=name, email=email, password=password, zip_code=zip_code)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return render_template('registration_sign_in.html', registration=False)


@app.route('/login', methods=["POST"])
def sign_in():
    """Login."""

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


@app.route('/activity/stored')
def get_stored_actvity():
    """Query for all activity existing within the bored application's database"""

    dict_list = []
    for u in crud.get_all_activities():
        temp_dict = {
            'activity_id': u.__dict__['activity_id'],
            'key': u.__dict__['key'],
            'activity': u.__dict__['activity'],
            'a_type': u.__dict__['a_type'],
            'participants': u.__dict__['participants'],
            'price': u.__dict__['price'],
            'link': u.__dict__['link'],
            'accessibility': u.__dict__['accessibility']
        }
        
        dict_list.append(temp_dict)

    return jsonify(dict_list)
    

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

    # Invoke helper functions to process values
    min_price = helper.convert_arg_to_percent(min_price)
    max_price = helper.convert_arg_to_percent(max_price)
    min_accessibility = helper.convert_arg_to_percent(min_accessibility)
    max_accessibility = helper.convert_arg_to_percent(max_accessibility)

    # Invoke helper functions to check min/max values
    min_price, max_price = helper.check_range_values(min_price, max_price)
    min_accessibility, max_accessibility = helper.check_range_values(min_accessibility, max_accessibility)        

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
        # Using data.get instead of data['error'] to prevent error if response object does not include 'error' key
        if data.get('error'):
            flash("This activity doesn't exist :(")
        else:
            flash("An error has occurred, please try again")

        return redirect("/")


@app.route('/activity/history')
def get_activity_by_user():
    """Get the activity history of browser's session user_id"""

    activity_dict = {}

    if "user_id" in session:
        user_history = crud.get_user_history(session["user_id"])
        for log in user_history:
            activity = crud.get_user_history_activity(log.activity_id)
            activity_dict[log.activity_id] = activity_dict.get(log.activity_id, activity.activity)
    else:
        flash('Please login to your account or register to have access to this feature.')

    return render_template('activity_history.html', user_history=user_history, activity_dict=activity_dict)


# Python3, only run the lines if server.py is ran directly
if __name__ == "__main__":
    connect_to_db(app)
    #Set app to run on debug mode at localhost ip address, and run the app
    app.run(host="0.0.0.0", debug=True)