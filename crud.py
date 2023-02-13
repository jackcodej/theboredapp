"""CRUD operations"""

from operator import and_
from model import db, User, History, Activity, connect_to_db
from sqlalchemy import desc, func
import datetime



def create_user(name, email, password, zip_code):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password, zip_code=zip_code)

    return user


def create_history_log(user_id, activity_id, last_clicked):
    """Create and return a new history log"""

    history_log = History(user_id=user_id, activity_id=activity_id, last_clicked=last_clicked)

    return history_log


def create_activity(key, activity, a_type, participants, price, link, accessibility):
    """Create and return a new activity."""

    activity = Activity(key=key, activity=activity, a_type=a_type, participants=participants, price=price, link=link, accessibility=accessibility)

    return activity


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_user_history(user_id):
    """Return a user's history descending order by date."""
    
    return History.query.filter(History.user_id == user_id).order_by(desc(History.last_clicked)).all()


def get_user_history_asc(user_id):
    """Return a user's history ascending order by date."""
    
    return History.query.filter(History.user_id == user_id).all()


def get_user_history_activity(activity_id):
    """Return an activity using it's id."""

    return Activity.query.filter(Activity.activity_id == activity_id).first()


def get_recent_activity():
    """Return all user's recent activity."""

    today = datetime.date.today().strftime("%B %d, %Y")
    a_week_ago = datetime.datetime.strptime(today, "%B %d, %Y") - datetime.timedelta(days=7)
    return History.query.filter(History.last_clicked > a_week_ago).order_by(desc(History.last_clicked)).all()


def get_all_activities():
    """Return all activities."""

    return Activity.query.all()


def get_activity_by_id(activity_id):
    """Return a specific activity by id."""

    return Activity.query.filter(Activity.activity_id == activity_id).first()


def get_activity_by_key(key):
    """Return a specific activity by key."""

    return Activity.query.filter(Activity.key == key).first()


def get_popular_activities():
    """Return a dictionary of most popular activity ids."""
    
    popular_dict = {}

    for log in History.query.all():
        popular_dict[log.activity_id] = popular_dict.get(log.activity_id, 0) + 1

    return popular_dict


def get_random_activities():
    """Return a list of random activities."""

    return Activity.query.order_by(func.random()).first()


def get_log_by_history_id(history_id):
    """Get history log by id."""

    return History.query.filter(History.history_id == history_id).first()
    

    # TODO: Need to use payload values to get activities that match
def get_filtered_activities(payload):
    """Get activity using payload to filter."""
    # Currently works for min/max values if they always exist but what about optional ones such as activity_type and participant number
    # May need a different function to handle a_type / participant number or figure out how to make this query dynamic and handle it
    return Activity.query.filter(Activity.accessibility <= payload['maxaccessibility'], Activity.accessibility >= payload['minaccessibility'], Activity.price <= payload['maxprice'], Activity.price >= payload['minprice']).first()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)