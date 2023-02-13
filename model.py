"""Models for the bored app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///activities", echo=True):
    """ Connect to our DB (local postgres db)"""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    zip_code = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class History(db.Model):
    """A user's history."""

    __tablename__ = "user_history"

    history_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.activity_id"))
    last_clicked = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User_History user_id={self.user_id} history_id={self.history_id}, activity_id={self.activity_id}, last_clicked={self.last_clicked}>'


class Activity(db.Model):
    """A activity"""

    __tablename__ = "activity"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key = db.Column(db.Integer, nullable=False, unique=True)
    activity = db.Column(db.String)
    # Named a_type instead of type to not overwrite 'type' namespace
    a_type = db.Column(db.String)
    participants = db.Column(db.Integer)
    price = db.Column(db.Float)
    link = db.Column(db.String)
    accessibility = db.Column(db.Float)

    def __repr__(self):
        return f'<Activity activity={self.activity}, a_type={self.a_type}, price={self.price}, accessibility={self.accessibility}, id={self.activity_id}>'


if __name__ == "__main__":
    from server import app

    # 'echo=False' will reduce program's SQLAlchemy output for queries
    connect_to_db(app)

    # Investigate why I needed to have this here --> Seems I need to have it everywhere
    # Root cause is it is flask says I am working beyond the context of my flask application
    # with app.app_context():
    #     db.create_all()