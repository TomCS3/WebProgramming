document.addEventListener('DOMContentLoaded', function() {
  like_function();
});

// Add an onclick listener to each of the like buttons
function like_function() {
  var LikesBtns = document.getElementsByClassName("like-btn");

  for (var i = 0; i < LikesBtns.length; i++) {
    LikesBtns[i].onclick = function() { 
      var post_id = this.dataset.post_id;
      like_btn_click(post_id)
    }
  }
}

// Update the post's likes
function like_btn_click(post_id) {
  var liked;
  var like_num = document.getElementById(`like-btn-${post_id}`).innerText.slice(0,1)
  if (document.getElementById(`like-btn-${post_id}`).classList.contains('btn-primary')) {
      liked = true;
  }
  else liked = false;

  // PUT request to update the post's likes in the database
  liked = !liked;
  fetch(`/posts/${post_id}/like`, {
    method: 'PUT',
    body: JSON.stringify({
      liked: liked
    })
  });

  // Update the onscreen likes
  if (liked == true) {
    document.getElementById(`like-btn-${post_id}`).classList.remove('btn-outline-primary');
    document.getElementById(`like-btn-${post_id}`).classList.add('btn-primary');
    like_num++
    document.getElementById(`like-btn-${post_id}`).innerText= like_num + ' Likes';
    
  }
  else {
    document.getElementById(`like-btn-${post_id}`).classList.remove('btn-primary');
    document.getElementById(`like-btn-${post_id}`).classList.add('btn-outline-primary');
    like_num--;
    document.getElementById(`like-btn-${post_id}`).innerText= like_num + ' Likes';
  }
}