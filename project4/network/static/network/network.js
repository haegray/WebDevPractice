
document.addEventListener('DOMContentLoaded', function() {

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
      compose();
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
  });
}
function compose() {

  document.querySelector('#tweets-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';


    var styles = `

.slide-up-now {
    opacity: 0;
    -webkit-animation: slide-up 1s cubic-bezier(0.4, 0, 0.2, 1) 500ms forwards;
  }
  
  
  @-webkit-keyframes slide-up {
          0% { -webkit-transform: translateY(100%); opacity: 1 }
          100% { -webkit-transform: translateY(0); opacity: 1  }
  }

  `

}