document.addEventListener('DOMContentLoaded', function() {
  follow_toggle();
});

// Add an onclick listener to each of the edit post buttons
function follow_toggle() {
  var followBtn = document.getElementById("follow-btn");
  followBtn.onclick = function() { 
    var profile_id = this.dataset.profile_id;
    follow_btn_click(profile_id)
  }
}

function follow_btn_click(profile_id) {
  var following;
  var followers_num = document.getElementById('followers-btn').innerText.slice(0,1)

  // Check if already following
  if (document.getElementById('follow-btn').classList.contains('btn-danger')) {
      following = true;
  }
  else following = false;

  // PUT request to update the users following
  following = !following;
  fetch(`/profile/${profile_id}/follow`, {
    method: 'PUT',
    body: JSON.stringify({
      following: following
    })
  });

  // Update the following btn and the number of followers on the page
  if (following == true) {
    document.getElementById('follow-btn').classList.remove('btn-outline-danger');
    document.getElementById('follow-btn').classList.add('btn-danger');
    document.getElementById('follow-btn').innerText= 'Following';
    followers_num++;
    document.getElementById('followers-btn').innerText= followers_num + ' Followers';
  }
  else {
    document.getElementById('follow-btn').classList.remove('btn-danger');
    document.getElementById('follow-btn').classList.add('btn-outline-danger');
    document.getElementById('follow-btn').innerText= 'Follow';
    followers_num--;
    document.getElementById('followers-btn').innerText= followers_num + ' Followers';
  }
}