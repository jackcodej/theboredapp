"""CRUD operations"""

from model import db, User, History, Activity, connect_to_db


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
    """Return a user by email"""

    return User.query.filter(User.email == email).first()


def get_user_history(user_id):
    """Return a user's history"""

    return History.query.filter(History.user_id == user_id).all()


# Incomplete need to use date time here
def get_recent_activity():
    """Return all user's recent activity"""
# Need to change the filter logic for the date and use present time
    return History.query.filter(History.last_clicked > 5).all()


def get_all_activities():
    """Return all activities"""

    return Activity.query.all()


def get_activity_by_id(activity_id):
    """Return a specific activity"""

    return Activity.query.filter(Activity.activity_id == activity_id).first()

# Query to get activity based on parameters


if __name__ == "__main__":
    from server import app

    connect_to_db(app)