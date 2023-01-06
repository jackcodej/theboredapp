// Makes js more strict, less convoluted
'use strict';

// Internal Activity Query
function getStoredActivities(){
    const activityContainer = document.querySelector('#user_activities');

    // empty textContent of activityContainer before adding new activities
    activityContainer.textContent = '';
    console.log('Stored Activities ran')
    fetch('/activity/stored')
    .then((response) => response.json())
    .then((activityData) =>{
        for (const activity of activityData){
            activityContainer.insertAdjacentHTML('beforeend', 
            `<div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
            <div class="card-header">${activity.a_type}</div>
            <div class="card-body">
              <p class="card-text">${activity.activity}</p>
              <p class="card-text">Participants: ${activity.participants}</p>
              <p class="card-text">Price: ${activity.price}</p>
              <p class="card-text">Link: ${activity.link}</p>
              <p class="card-text">Accessibility: ${activity.accessibility}</p>
            </div>
          </div>`
            );
        }
    });
}

if (document.querySelector('#get_activities')){
    document.querySelector('#get_activities').addEventListener('click', getStoredActivities);
}

// TODO: getRandomActivities
// TODO: getPopularActivities