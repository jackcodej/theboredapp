// Makes js more strict, less convoluted
'use strict';

// Internal Activity Query
function getStoredActivities(){
    const activityContainer = document.querySelector('#user_activities')
    console.log('Stored Activities ran')
    fetch('/activity/stored')
    .then((response) => response.json())
    .then((activityData) =>{
        console.log(activityData);
        for (const activity of activityData){
            activityContainer.insertAdjacentHTML('beforeend', 
            `<ul>
            <li>Activity: ${activity.activity}</li>
            <li>Key: ${activity.key}</li>
            <li>Activity Type: ${activity.a_type}</li>
            <li>Participants: ${activity.participants}</li>
            <li>Price: ${activity.price}</li>
            <li>Link: ${activity.link}</li>
            <li>Accessibility: ${activity.accessibility}</li>
            </ul>`
            );
        }
    });
}

document.querySelector('#get_activities').addEventListener('click', getStoredActivities);