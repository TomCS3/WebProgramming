document.addEventListener('DOMContentLoaded', function() {
  post_edit_links();
});

// Add an onclick listener to each of the edit post buttons
function post_edit_links() {
  var editBtns = document.getElementsByClassName("edit-link");

  for (var i = 0; i < editBtns.length; i++) {
    editBtns[i].onclick = function() { 
      var post_id = this.dataset.post_id;
      edit_btn_click(post_id)
    }
  }
}

// Hide the post and create a form to edit the post
function edit_btn_click(post_id) {

  // Hide the post content and edit post button
  document.getElementById(`post-content-${post_id}`).style.display = 'none';
  document.getElementById(`edit-link-${post_id}`).remove();

  // Create the textarea, preloads the existing content and add a save button
  var content = document.getElementById(`post-content-text-${post_id}`).innerText;
  var edit_box = document.createElement('textarea');
  edit_box.setAttribute('id', `edit-form-box-${post_id}`);
  edit_box.setAttribute('class', 'form-control my-2');
  edit_box.value = content;

  var edit_btn = document.createElement('button');
  edit_btn.setAttribute('id', `edit-form-btn-${post_id}`);
  edit_btn.setAttribute('class', 'btn btn-primary btn-sm');
  edit_btn.setAttribute('data-', `${post_id}`);
  var btn_text = document.createTextNode("Save");

  document.getElementById(`edit-form-${post_id}`).appendChild(edit_box);
  document.getElementById(`edit-form-${post_id}`).appendChild(edit_btn);
  document.getElementById(`edit-form-btn-${post_id}`).appendChild(btn_text);

  // Add an onclick listener for the save button
  edit_btn.onclick = () => post_edit(post_id);
}

// Update the post content and display the post
function post_edit(post_id) {
  var content = document.getElementById(`edit-form-box-${post_id}`).value;

  // PUT request to update the post
  fetch(`/posts/${post_id}/edit`, {
    method: 'PUT',
    body: JSON.stringify({
      content: content
    })
  });

  // Update the on page post content 
  document.getElementById(`edit-form-box-${post_id}`).remove();
  document.getElementById(`edit-form-btn-${post_id}`).remove();
  document.getElementById(`post-content-text-${post_id}`).innerText = content;
  document.getElementById(`post-content-${post_id}`).style.display = 'block';

  // Recreate the edit link
  var edit_link = document.createElement('small');
  edit_link.setAttribute('class', 'btn btn-link edit-link');
  edit_link.setAttribute('id', `edit-link-${post_id}`);
  document.getElementById(`metadata-info-${post_id}`).appendChild(edit_link);
  document.getElementById(`edit-link-${post_id}`).innerHTML = "Edit";
  
  // Add an onclick listener to the edit post button
  document.getElementById(`edit-link-${post_id}`).onclick = () => edit_btn_click(post_id);
  var content = document.getElementById(`post-content-text-${post_id}`).innerText;
}
