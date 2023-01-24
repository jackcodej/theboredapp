# theboredapp

The goal of this application is to use flask, jinja, and alchemy to produce a single page web application.

1. The application will allow users to create and sign into their accounts.
2. Query for an activity based upon the arguments their provide.
3. Store the history of activities queried by users
4. Provide suggestions to users based upon previously chosen activities


Data model
https://drive.google.com/file/d/1bMAIegmceO4nNb6xsBEQsIz-nzQexSHC/view?usp=sharing


Clickup Sprint 1 Taskboard
https://sharing.clickup.com/42117773/l/h/6-240216916-1/25d3324c1f6bae6
Clickup Sprint 2 Taskboard
https://sharing.clickup.com/42117773/l/h/6-900900195592-1/5622256421df765
Clickup Post HackBright Sprint Taskboard
https://sharing.clickup.com/42117773/l/h/6-900900195603-1/d5f4bd73b9be481


1/24/2023
A full stack web application, using a python flask server with sqlalchemy to facilitate communication with a postgresql database.
The front end uses AJAX to dynamically display content, bootstrap for styling, React for controlled form components, and Jinja for templating.

Complete Features
1. Users can register for an account and signed into their accounts.
2. Users can query for a random activity or provide arguments for a more specified activity
3. Users that are signed in have access to all previously accessed activities
4. Users can interact with their history by removing records or reaching the activity itself through the history log
5. The home page provides suggestions to users, only activities that exist in the bored app's activity table
6. The home page provides a social carousel section displaying all activities chosen by users within the past 7 days
7. The home page provides a popular carousel section displaying the most popular activities (top 5)