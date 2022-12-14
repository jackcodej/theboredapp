"""Script to seed database."""

import os
import json

import model
import server
import crud

os.system("dropdb activities")
os.system("createdb activities")

model.connect_to_db(server.app)
model.db.create_all()

# Load test user data from JSON file
with open("data/users.json") as f:
    user_data = json.loads(f.read())

# Load activities from JSON file
with open ("data/test_activities.json") as g:
    activity_data = json.loads(g.read())

# Load test user history from JSON file
with open ("data/histories.json") as h:
    history_data = json.loads(h.read())

# Create a list of users to add to database
user_list = []
# Loop through each user in user data and grabs name,email,password,zip_code
for user in user_data:
    name, email, password, zip_code = (
        user["name"],
        user["email"],
        user["password"],
        user["zip_code"],
    )
# Create a new user using extracted information and append it to user_list
    db_user = crud.create_user(name, email, password, zip_code)
    user_list.append(db_user)


# Create a list of activities to add to database
activity_list = []
for activity in activity_data:
    key, activity, a_type, participants, price, link, accessibility = (
        activity["key"],
        activity["activity"],
        activity["type"],
        activity["participants"],
        activity["price"],
        activity["link"],
        activity["accessibility"],
    )

    db_activity = crud.create_activity(key, activity, a_type, participants, price, link, accessibility)
    activity_list.append(db_activity)

# Create test record for user history
history_list = []
for log in history_data:
    user_id, activity_id, last_clicked = (
        log["user_id"],
        log["activity_id"],
        log["last_clicked"],
    )

    db_history_log = crud.create_history_log(user_id=user_id, activity_id= activity_id, last_clicked=last_clicked)
    history_list.append(db_history_log)
        
model.db.session.add_all(user_list)
model.db.session.add_all(activity_list)
model.db.session.commit()
#History is dependent on FK from user_list and activity_list so it needs to exist first
model.db.session.add_all(history_list)
model.db.session.commit()