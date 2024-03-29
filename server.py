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

# Store alternate text
alt_text_dict = {
'busywork': 'A variety of yarn organized by color in a grid of wooden cupboards',
'charity': 'Hands from 5 people on a wooden table, alternating sides',
'cooking': 'Aerial view of a cooking table with a variety of ingredients and a large wood cutting board',
'diy': 'A wooden wall with several mounted tools',
'education': 'A wall of books that curve inwards',
'music': 'A home recording studio featuring several instruments',
'recreational': 'A group of people walking on a hiking trail next to tall trees',
'relaxation': 'A woman relaxing on a hammock during sunset next to a pond',
'social': 'A group pf people socializing over drinks'
}

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
        update_favorites()
        flash(f"Welcome back, {user.name}")

    return redirect("/")

# TODO: Add additional validation and make the form match the query for an activity, for consistency!
@app.route('/add-activity', methods=["POST"])
def add_activity():
    """Add an activity."""

    activity = request.form.get("activity")
    accessibility = request.form.get("accessibility")
    # Convert english accessibility level to numerical.
    if accessibility == "few-to-no":
        accessibility = 33
    elif accessibility == "minor":
        accessibility = 66
    else:
        accessibility = 100
    type = request.form.get("a_type")
    participants = request.form.get("participants")
    price = request.form.get("price")
    link = request.form.get("link")

    if not crud.get_activity_by_name(activity):
        new_activity = crud.create_activity(activity=activity, a_type=type, participants=participants, price=price, link=link, accessibility=accessibility, key=None)
        db.session.add(new_activity)
        db.session.commit()
    else:
        flash("The proposed activity already exists! Here is the activity, favorite it to access quickly in the future or check your history!")
        new_activity = crud.get_activity_by_name(activity)

    try:
        new_history_log = crud.create_history_log(user_id=session["user_id"], 
                                                activity_id=new_activity.activity_id, 
                                                last_clicked=date.today().strftime("%B %d, %Y")
                                                )
        db.session.add(new_history_log)
        db.session.commit()
    except:
        flash("An error has occurred, please try again (add-activity)")

    return render_template('activity.html', activity=new_activity, alt_text_dict=alt_text_dict, favorites=session["favorites"])
    

@app.route('/activity/random')
def get_random_activity():
    """Returns 6 random activities."""

    random_activities = []

    for _ in range(6):
        random_activities.append(helper.map_activity_to_dict(crud.get_random_activities()))

    return jsonify(random_activities)


@app.route('/activity/<activity_id>')
def get_activity_by_id(activity_id):
    """Get an activity by id"""
    
    activity = crud.get_activity_by_id(activity_id)
    try:
        # If user is signed in create a new record in history
        if "user_id" in session:
            new_history_log = crud.create_history_log(user_id=session["user_id"], 
                                                    activity_id=activity_id, 
                                                    last_clicked=date.today().strftime("%B %d, %Y")
                                                    )
            db.session.add(new_history_log)
            db.session.commit()
        return render_template('activity.html', activity=activity, alt_text_dict=alt_text_dict, favorites=session["favorites"])
    except:
        flash("An error has occurred, please try again (get_activity_by_id)")

    return render_template('activity.html', activity=activity, alt_text_dict=alt_text_dict, favorites=session["favorites"])


@app.route('/activity/popular')
def get_popular_activity():
    """Return most popular activities."""
    
    popular_activities = []
    popular_dict = crud.get_popular_activities()

    # Sort the dictionaries
    sorted_popular_dict = sorted(popular_dict.items(), key=lambda x:x[1])
    # Append the most popular activity_id (top 5) to popular_activities
    if len(sorted_popular_dict) > 5:
        for x in range(-1,-6,-1):
            popular_activities.append(helper.map_activity_to_dict(activity = crud.get_activity_by_id(sorted_popular_dict[x][0])))
    else:
        # Print all available activities if less than 5
        for x in range(len(sorted_popular_dict)):
            popular_activities.append(helper.map_activity_to_dict(activity = crud.get_activity_by_id(sorted_popular_dict[x][0])))

    return jsonify(popular_activities)


@app.route('/activity/stored')
def get_recent_activity():
    """Query for recent activity, past week."""

    dict_list = []
    for history_activity_log in crud.get_recent_activity():
        dict_list.append(helper.map_activity_to_dict(crud.get_activity_by_id(history_activity_log.__dict__['activity_id'])))
    return jsonify(dict_list)


@app.route('/remove/history/<history_id>')
def remove_by_history_id(history_id):
    """Delete from user history."""

    try:
        del_log = crud.get_log_by_history_id(history_id)
        db.session.delete(del_log)
        db.session.commit()
        flash(f"The activity was removed from your history")
    except:
        flash("An error has occurred, please try again (remove_by_history_id)")

    return get_activity_by_user()



@app.route('/add/favorite/<activity_id>')
def add_favorite_by_activity_id(activity_id):
    """Add favorite status to an activity."""

    try:
            new_favorite = crud.create_favorite(user_id=session["user_id"], activity_id=activity_id)
            db.session.add(new_favorite)
            db.session.commit()
    except:
        flash("An error has occured, please try again (add_favorite_by_activity_id)")
    update_favorites()

    return redirect("/")


@app.route('/remove/favorite/<activity_id>')
def remove_favorite_by_activity_id(activity_id):
    """Remove favorite status from an activity."""

    try:
        crud.remove_favorite_status(session["user_id"], activity_id)
    except:
        flash("An error has occured, please try again (remove_favorite_by_activity_id)")
    update_favorites()

    return get_favorites_by_user()


@app.route('/activity/search')
def find_filtered_activity():
    """Query for an activity from theboredapp with arguments"""

    # Get all values from form **Not request.form because this is not a post request
    # key = request.args.get('key', '') depricated
    # TODO: Change range values on form from range slider to a select menu and convert values to numerical value, may need to make changes to crud.get_filtered_activites
    a_type = request.args.get('a_type', '')
    participants = request.args.get('participants', '')
    min_price = 0
    max_price = request.args.get('max_price', 100)
    min_accessibility = 0
    max_accessibility = request.args.get('max_accessibility', 100)

    # Invoke helper functions to process values
    max_price = helper.convert_arg_to_percent(max_price)
    max_accessibility = helper.convert_arg_to_percent(max_accessibility)

    # Invoke helper functions to check min/max values
    min_price, max_price = helper.check_range_values(min_price, max_price)
    min_accessibility, max_accessibility = helper.check_range_values(min_accessibility, max_accessibility)        

    payload = {
        'type': a_type,
        'participants': participants,
        'minprice': min_price,
        'maxprice': max_price,
        'minaccessibility': min_accessibility,
        'maxaccessibility': max_accessibility,
    }

    try:
        # Get activity from DB and add it to history if user is signed in
        activity = crud.get_filtered_activities(payload)
        # If user is signed in create a new record in history
        if "user_id" in session:
            new_history_log = crud.create_history_log(user_id=session["user_id"], 
                                                    activity_id=activity.activity_id, 
                                                    last_clicked=date.today().strftime("%B %d, %Y")
                                                    )
            db.session.add(new_history_log)
            db.session.commit()
        return render_template('activity.html', activity=activity, alt_text_dict=alt_text_dict, favorites=session["favorites"])
    except:
        # Using data.get instead of data['error'] to prevent error if response object does not include 'error' key
        flash("An error has occurred, please try again (find_filtered_activity)")

        return redirect("/")


@app.route('/activity/history')
def get_activity_by_user():
    """Get the activity history of browser's session user_id"""

    activity_dict = {}
    if "user_id" in session:
        user_history = crud.get_user_history(session["user_id"])
        for log in user_history:
            activity_info = []
            activity_info.append(crud.get_user_history_activity(log.activity_id))
            activity_dict[log.activity_id] = activity_dict.get(log.activity_id, activity_info)
    else:
        flash('Please login to your account or register to have access to this feature.')

    return render_template('activity_history.html', user_history=user_history, activity_dict=activity_dict, alt_text_dict=alt_text_dict)


@app.route('/activity/favorites')
def get_favorites_by_user():
    """Get the favorite activities of the user"""

    activity_dict = {}
    if "user_id" in session:
        try:
            user_favorites = crud.get_user_favorites(session["user_id"])
            for favorite in user_favorites:
                activity_info = []
                activity_info.append(favorite)
                activity_dict[favorite.activity_id] = activity_dict.get(favorite.activity_id, crud.get_activity_by_id(favorite.activity_id))
        except:
            flash('No favorites found, please favorite an activity before trying this feature.')
    else:
        flash('Please login to your account or register to have access to this feature.')
    update_favorites()

    return render_template('favorite_activities.html', activity_dict=activity_dict, alt_text_dict=alt_text_dict)


def update_favorites():
    """Store latest favorites of the user"""

    f = []
    for favorite in crud.get_user_favorites(session["user_id"]):
        f.append(favorite.activity_id)
    session["favorites"] = f


@app.route('/activity/add')
def show_add_activity():
    """Navigate to the add activity page"""

    return render_template('add_activity.html')


# Python3, only run the lines if server.py is ran directly
if __name__ == "__main__":
    connect_to_db(app)
    #Set app to run on debug mode at localhost ip address, and run the app
    app.run(host="0.0.0.0", debug=True)