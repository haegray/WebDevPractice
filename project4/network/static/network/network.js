
document.addEventListener('DOMContentLoaded', function() {
  //document.querySelector('#tweets-view').style.display = 'block';
  //document.querySelector('#compose-view').style.display = 'none';

    // By default, load the inbox
  // Use buttons to toggle between views

  document.addEventListener('click', function(e){
  console.log("target ", e.target.id)
  if(e.target.id === 'label-like-button'){
  
    let row_post = e.target.parentElement.parentElement;
    row_post.classList.toggle('active');
    let active = row_post.classList.contains('active');

    e.target.classList.toggle('checked');
    like(row_post.id, active);
  } else if(e.target.id === 'compose-button'){
    cmpview = document.querySelector('#compose-view');
    cmpview.style.display = cmpview.style.display === 'block' ? "none" : "block";
    cmpview.classList.toggle('backwards');
    cmpview.classList.toggle('forwards');
    cmpview.style.animationPlayState = 'running';
    document.addEventListener('click', function(e){
      if(e.target.id === 'tweet-button'){
        e.preventDefault();
        cmpview.classList.toggle('forwards');
        cmpview.classList.toggle('backwards');
        cmpview.style.animationPlayState = 'running';
        cmpview.addEventListener('animationend', () => {
          cmpview.classList.toggle('backwards');
          cmpview.classList.toggle('forwards');
          cmpview.style.display = cmpview.style.display === 'none' ? "block" : "none";
          document.querySelector('#tweet-form').submit();
        });
      }
    });
  } else if (e.target.id === 'follow-button'){
      profile_name = document.querySelector('.profile-username').id;
      follow(profile_name);
      
  }
  });
});

function like(post, active){
  let str = '/posts/' + post;
  console.log("String is ",str);
  fetch(str, {
    method: 'PUT',
    body: JSON.stringify({
        like: Number(active)
    })
  }).then(response => response.json())
  .then(json => {
    console.log("JSON ", json)
    likesContainer = document.getElementById(post).querySelector('#post-likes')
    console.log("container ", likesContainer.innerText)
    likesContainer.innerText = `${json.likes}`;  
  });
}

function follow(profile_name){

  let str = '/profile/' + profile_name;
  console.log("String is ",str);
  fetch(str, {
    method: 'PUT',
    body: JSON.stringify({
        profile: profile_name
    })
  }).then(response => response.json())
  .then(json => {
    console.log("JSON ", json)
    followButton = document.querySelector('#follow-button')
    console.log("followButton ", followButton.value)
    followButton.value = `${json.following}`;  

    followers = document.querySelector('#follow-stats')
    followers.innerText = `${json.num_followers} followers`; 
  });
}
