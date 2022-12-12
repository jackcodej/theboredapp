"""Script to seed database."""

import os
import json

import model
import server
import crud

os.system("dropdb activities")
os.system("createdb activities")

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

#Load user data from JSON file
with open("data/users.json") as f:
    user_data = json.loads(f.read())

#Create users, store them in a list
user_list = []
for user in user_data:
    name, email, password, zip_code = (
        user["name"],
        user["email"],
        user["password"],
        user["zip_code"],
    )

    db_user = crud.create_user(name, email, password, zip_code)
    with server.app.app_context():
        user_list.append(db_user)
        
with server.app.app_context():
    model.db.session.add_all(user_list)
    model.db.session.commit()