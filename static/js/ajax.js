// Makes js more strict, less convoluted
'use strict';

// Internal Activity Query
function getStoredActivities(){
    const targetActivityContainer = document.querySelector('#user_activities');

    // empty textContent of targetActivityContainer before adding new activities
    targetActivityContainer.textContent = '';
    fetch('/activity/stored')
    .then((response) => response.json())
    .then((activityData) =>{
        for (const activity of activityData){
            targetActivityContainer.insertAdjacentHTML('beforeend', 
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

if (document.querySelector('#user_activities')){
    window.addEventListener('load', getStoredActivities);
}

function getPopularActivities(){
    const targetActivityContainer = document.querySelector('#popular_activities');

    targetActivityContainer.textContent = '';
    fetch('/activity/popular')
    .then((response) => response.json())
    .then((activityData) =>{
        for (const activity of activityData){
            targetActivityContainer.insertAdjacentHTML('beforeend', 
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

if (document.querySelector('#popular_activities')){
    window.addEventListener('load', getPopularActivities);
}


function getRandomActivities(){
    const targetActivityContainer = document.querySelector('#suggested_activities');

    targetActivityContainer.textContent = '';
    fetch('/activity/random')
    .then((response) => response.json())
    .then((activityData) =>{
      console.log("pewpewactivityData", activityData)
        for (const activity of activityData){
            targetActivityContainer.insertAdjacentHTML('beforeend', 
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

if (document.querySelector('#suggested_activities')){
    window.addEventListener('load', getRandomActivities);
}
if (document.querySelector('#get_suggested_activities')){
  document.querySelector('#get_suggested_activities').addEventListener('click', getRandomActivities);
}