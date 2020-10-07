document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send the email when the compose form is submitted
  document.querySelector('#compose-form').onsubmit = send_email;
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get each email in the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => mailbox_row(email));
  });
}

function mailbox_row(email) {

  // Create a div container for one email
  const box = document.createElement('div');
  box.setAttribute('id', email.id);
  box.setAttribute('class', 'container box')

  // Create an attributes row within the container and style
  const attrs = document.createElement('div');
  attrs.setAttribute('id', `${email.id}-attrs`);
  attrs.setAttribute('class', 'row')
  attrs.style.backgroundColor = email.read ? '#D3D3D3': 'white'; 

  // Create a column for the sender, subject and timestamp
  const sender = document.createElement('div');
  sender.setAttribute('class', 'col-3 sender');
  sender.innerHTML = email.sender;
  const subject = document.createElement('div');
  subject.setAttribute('class', 'col-6 subject');
  subject.innerHTML = email.subject;
  const timestamp = document.createElement('div');
  timestamp.setAttribute('class', 'col-3 timestamp');
  timestamp.innerHTML = email.timestamp;

  // On-click event listner for viewing an email 
  box.addEventListener('click', () => view_email(email.id));

  // Create the each email's row for the mailbox
  document.querySelector('#emails-view').append(box);
  document.getElementById(email.id).appendChild(attrs);
  document.getElementById(`${email.id}-attrs`).appendChild(sender);
  document.getElementById(`${email.id}-attrs`).appendChild(subject);
  document.getElementById(`${email.id}-attrs`).appendChild(timestamp);
}

function view_email(email_id) {

  // Retrieve individual email via Get
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    // Show the email view and hide the rest
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Render the email
    document.getElementById('email-subject').innerHTML = email.subject;
    document.getElementById('email-timestamp').innerHTML = email.timestamp;
    document.getElementById('email-sender').innerHTML = email.sender;
    document.getElementById('email-recipients').innerHTML = email.recipients;
    document.getElementById('email-body').innerHTML = email.body;

    // Mark as read via PUT
    if(!email.read) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    }
  });
}

function send_email() {

  // Retrieves the data from the form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Sends an email via a POST request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      load_mailbox('sent');
  });
  
  return false;
}