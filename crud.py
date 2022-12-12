"""CRUD operations"""

from model import db, User, History, Activity, connect_to_db


def create_user(name, email, password, zip_code):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password, zip_code=zip_code)

    return user


def create_history_log(history_id, user_id, activity_key, last_clicked):
    """Create and return a new history log"""

    history_log = History(history_id=history_id, user_id=user_id, activity_key=activity_key, last_clicked=last_clicked)

    return history_log


if __name__ == "__main__":
    from server import app

    connect_to_db(app)