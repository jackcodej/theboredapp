// Makes js more strict, less convoluted
'use strict';

function getRandomActivities(){
  const targetActivityContainer = document.querySelector('#suggested_activities');
  targetActivityContainer.textContent = '';
  let first = true;

  fetch('/activity/random')
  .then((response) => response.json())
  .then((activityData) =>{
      for (const activity of activityData){
        if (first){
          targetActivityContainer.insertAdjacentHTML('beforeend', 
          `<div class="carousel-item active"><div class="card text-white bg-dark">
          <div class="card-header">${activity.activity}</div>
          <div class="card-body">
          <p class="card-text">${activity.a_type}</p>
            <p class="card-text">Participants: ${activity.participants}</p>
            <p class="card-text">Price: ${activity.price}</p>
            <p class="card-text">Link: ${activity.link}</p>
            <p class="card-text">Accessibility: ${activity.accessibility}</p>
          </div>
          <button type="button" class="btn btn-info card-button" value="goTobtn-light"><a href="/activity/${activity.activity_id}">Read more</a></button>
          </div></div>`
          );
          first = false;
        } else{
          targetActivityContainer.insertAdjacentHTML('beforeend', 
          `<div class="carousel-item"><div class="card text-white bg-dark">
          <div class="card-header">${activity.activity}</div>
          <div class="card-body">
          <p class="card-text">${activity.a_type}</p>
          <p class="card-text">Participants: ${activity.participants}</p>
          <p class="card-text">Price: ${activity.price}</p>
          <p class="card-text">Link: ${activity.link}</p>
          <p class="card-text">Accessibility: ${activity.accessibility}</p>
          </div>
          <button type="button" class="btn btn-info card-button" value="goToActivity"><a href="/activity/${activity.activity_id}">Read more</a></button>
          </div></div>`
          );
        }
      }
    });
  }
    
    if (document.querySelector('#suggested_activities')){
      window.addEventListener('load', getRandomActivities);
    }
    if (document.querySelector('#get_suggested_activities')){
      document.querySelector('#get_suggested_activities').addEventListener('click', getRandomActivities);
    }


function getPopularActivities(){
    const targetActivityContainer = document.querySelector('#popular_activities');
    targetActivityContainer.textContent = '';
    let first = true;

    fetch('/activity/popular')
    .then((response) => response.json())
    .then((activityData) =>{
        for (const activity of activityData){
          if (first){
            targetActivityContainer.insertAdjacentHTML('beforeend', 
            `<div class="carousel-item active"><div class="card text-white bg-dark mb-1">
            <div class="card-header">${activity.activity}</div>
            <div class="card-body">
            <p class="card-text">${activity.a_type}</p>
              <p class="card-text">Participants: ${activity.participants}</p>
              <p class="card-text">Price: ${activity.price}</p>
              <p class="card-text">Link: ${activity.link}</p>
              <p class="card-text">Accessibility: ${activity.accessibility}</p>
            </div>
            <button type="button" class="btn btn-info card-button" value="goToActivity"><a href="/activity/${activity.activity_id}">Read more</a></button>
          </div></div>`
            );
            first = false;
          } else{
            targetActivityContainer.insertAdjacentHTML('beforeend', 
            `<div class="carousel-item"><div class="card text-white bg-dark mb-1">
            <div class="card-header">${activity.activity}</div>
            <div class="card-body">
            <p class="card-text">${activity.a_type}</p>
              <p class="card-text">Participants: ${activity.participants}</p>
              <p class="card-text">Price: ${activity.price}</p>
              <p class="card-text">Link: ${activity.link}</p>
              <p class="card-text">Accessibility: ${activity.accessibility}</p>
            </div>
            <button type="button" class="btn btn-info card-button" value="goToActivity"><a href="/activity/${activity.activity_id}">Read more</a></button>
          </div></div>`
            );
          }
        }
    });
}
    
    if (document.querySelector('#popular_activities')){
        window.addEventListener('load', getPopularActivities);
    }


    // Internal Activity Query
function getStoredActivities(){
  const targetActivityContainer = document.querySelector('#user_activities');
  let s_first = true;
  // empty textContent of targetActivityContainer before adding new activities
  targetActivityContainer.textContent = '';
  fetch('/activity/stored')
  .then((response) => response.json())
  .then((activityData) =>{
      for (const activity of activityData){
        if (s_first){
          targetActivityContainer.insertAdjacentHTML('beforeend', 
          `<div class="carousel-item active"><div class="card text-white bg-dark mb-1">
          <div class="card-header">${activity.activity}</div>
          <div class="card-body">
          <p class="card-text">${activity.a_type}</p>
            <p class="card-text">Participants: ${activity.participants}</p>
            <p class="card-text">Price: ${activity.price}</p>
            <p class="card-text">Link: ${activity.link}</p>
            <p class="card-text">Accessibility: ${activity.accessibility}</p>
          </div>
          <button type="button" class="btn btn-info card-button" value="goToActivity"><a href="/activity/${activity.activity_id}">Read more</a></button>
        </div></div>`
          );
          s_first = false;
        } else{
          targetActivityContainer.insertAdjacentHTML('beforeend', 
          `<div class="carousel-item"><div class="card text-white bg-dark mb-1">
          <div class="card-header">${activity.activity}</div>
          <div class="card-body">
          <p class="card-text">${activity.a_type}</p>
            <p class="card-text">Participants: ${activity.participants}</p>
            <p class="card-text">Price: ${activity.price}</p>
            <p class="card-text">Link: ${activity.link}</p>
            <p class="card-text">Accessibility: ${activity.accessibility}</p>
          </div>
          <button type="button" class="btn btn-info card-button" value="goToActivity"><a href="/activity/${activity.activity_id}">Read more</a></button>
        </div></div>`
          );
        }
      }
  });
}

if (document.querySelector('#user_activities')){
    window.addEventListener('load', getStoredActivities);
}


function thumbs_down(x) {
  x.classList.toggle("fa-thumbs-down");
}
function thumbs_up(x) {
  x.classList.toggle("fa-thumbs-up");
}