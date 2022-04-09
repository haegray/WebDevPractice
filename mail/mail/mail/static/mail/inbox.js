function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

document.addEventListener('DOMContentLoaded', function() {

    // By default, load the inbox
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  load_mailbox("inbox");
});

function compose_email(email_now) {


  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').disabled = false;
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
 
  if(email_now !== "" && email_now.subject !== undefined && email_now.subject !== ""){
    document.querySelector('#compose-recipients').value = email_now.sender;
    if(!email_now.subject.startsWith('Re:')){
      document.querySelector('#compose-subject').value = "Re: " + email_now.subject;
    } else {
      document.querySelector('#compose-subject').value = email_now.subject;
    }
    document.querySelector('#compose-body').value = email_now.body;

    document.querySelector('#compose-recipients').disabled = true;
    document.querySelector('#compose-subject').disabled = true;
  }

  //Get email and send email
    document.querySelector('#compose-form').onsubmit = function() {

      
      const recipients = document.querySelector('#compose-recipients').value;
      const subject = document.querySelector('#compose-subject').value;
      const body = "\n On " + new Date() + " " + document.querySelector('#compose-sender').value + " wrote: " + document.querySelector('#compose-body').value + "\n";
     
      
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body,
            read: false
        })
      })
      .then(response => response.text())
      .then(result => {
        console.log(result);
        load_mailbox("sent");
      });

      
      return false;
    }
    
}

function show_emails(mailbox, emails) {


  var styles = `
  * {
    box-sizing: border-box;
  }

  @keyframes archive {
    0% {
        opacity: 1;
        height: 100%;
        line-height: 100%;
        padding: 20px;
        margin-bottom: 10px;
    }
    75% {
        opacity: 0;
        height: 100%;
        line-height: 100%;
        padding: 20px;
        margin-bottom: 10px;
    }
    100% {
        opacity: 0;
        height: 0px;
        line-height: 0px;
        padding: 0px;
        margin-bottom: 0px;
    }
}

  /* Create three equal columns that floats next to each other */
  .column {
    display: flex;
    align-items: center;
    width: 30%;
    padding: 10px;
    height: 50px;
    overflow: hidden;
    white-space: nowrap;
    
  }

  #zero-col{
    width: 10%;
  }

  #zero-col-read{
    display: flex;
    align-items: left;
    padding:0px;
    margin-left: -10px;
    inline-size: 150px;
    overflow-wrap: break-word;
  }

  /* Clear floats after the columns */
  .row:after {
    content: "";
    display: table;
    clear: both;
  }

  .row{
    animation-name: archive;
    animation-duration: 2s;
    animation-fill-mode: forwards;
    animation-play-state: paused;
  }

  .aux-button {
    margin: 2px;
    padding: 7px;
    background-color: white;
    color: #4169E1;
    border-color: #4169E1;
    border-width: thin;
    border-radius: 3px;
    -webkit-box-shadow: none;
	  -moz-box-shadow: none;
	  box-shadow: none;
  }
  
  #archive-button {
    margin: 2px;
    padding: 7px;
    background-color: white;
    color: #4169E1;
    border-color: #4169E1;
    border-width: thin;
    border-radius: 3px;
    -webkit-box-shadow: none;
	  -moz-box-shadow: none;
	  box-shadow: none;
  }

`

  var styleSheet = document.createElement("style");
  styleSheet.innerText = styles;
  document.head.appendChild(styleSheet);


  for (let i = 0; i < emails.length; i++) {
    let email_now = emails[i];

    const element = document.createElement('div');
    element.className = 'row';
    element.id = 'email-' + email_now.id;

    
    if(email_now.read===true){
      element.style.backgroundColor = "#DCDCDC";
    } 

    // element.innerHTML = 'This is the content of the div.';

    let col_zero = document.createElement('div');
    col_zero.className = 'column';
    col_zero.id = 'zero-col';

    var button_archive = document.createElement('input'),
    archive = "archive";

    if(email_now.archived){
      archive = "unarchive";
    } 

    button_archive.type  = 'button';
    button_archive.value = archive;
    button_archive.id = "archive-button";
    col_zero.appendChild(button_archive);
    element.append(col_zero);
    button_archive.addEventListener('click', () => {
    let str = '/emails/' + email_now.id;
    console.log(str);
    fetch(str, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !email_now.archived
      })
    })

    console.log(element.parentElement);
    console.log(element);
      element.style.animationPlayState = 'running';
      element.addEventListener('animationend', () => {
      document.querySelector('#' + element.id).remove();
      });

    });

   

    
    let col_one = document.createElement('div');
    col_one.className = 'column';

    if(mailbox === "inbox"){
      const sender = document.createElement("b");
      sender.textContent = "Sender: "
      let sender_text = document.createElement("span");
      sender_text.textContent = email_now.sender;
      col_one.appendChild(sender);
      col_one.appendChild(sender_text);
      
    } else {
      const recipients = document.createElement("b");
      recipients.textContent = "Recipients: "
      let recipients_text = document.createElement("span");
      recipients_text.textContent = email_now.recipients[0];
      col_one.appendChild(recipients);
      col_one.appendChild(recipients_text);
      
    }
    
    element.append(col_one);
    let col_two = document.createElement('div');
    col_two.className = 'column';

    const subject = document.createElement("b");
    subject.textContent = "Subject: ";
    let subject_text = document.createElement("span");
    subject_text.textContent = email_now.subject;

    
    col_two.appendChild(subject);
    col_two.appendChild(subject_text);
    element.append(col_two);

    let col_three = document.createElement('div');
    col_three.className = 'column';

    let timestamp = document.createElement("b");
    timestamp.textContent =  "Timestamp: ";
    let timestamp_text = document.createElement("span");
    timestamp_text.textContent = email_now.timestamp;

    col_three.appendChild(timestamp);
    col_three.appendChild(timestamp_text);
    
    element.append(col_three);
  
    document.querySelector('#emails-view').append(element);
    element.addEventListener('click', function(e){
      console.log(e.target);
      console.log(e.currentTarget);
      console.log(e.target.parentElement);
      console.log(document.getElementById('archive-button').clicked);
      if(e.target.id !== 'archive-button'){
        view_email(mailbox, email_now);
      }
    });
  }
}

function view_email(mailbox, email_now){
  str = '/emails/' + email_now.id
  fetch(str, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  document.querySelector('#compose-view').style.display = 'none';

  const myNode = document.querySelector('#emails-view');
  myNode.innerHTML = '';

  let element = document.createElement('div');
  element.className = 'row';
  
  let col_zero = document.createElement('div');
  col_zero.className = 'column';
  col_zero.id = "zero-col-read";

  var button = document.createElement('input'),
    archive = "archive";

    if(email_now.archived){
      archive = "unarchive";
    } 

  button.type  = 'button';
  button.value = archive;
  button.className = "aux-button";
  button.addEventListener('click', () => {
    let str = '/emails/' + email_now.id;
    console.log(str);
    fetch(str, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !email_now.archived
      })})
      .then(result => {
        console.log(result);
        load_mailbox(mailbox);
      });
  });


  col_zero.appendChild(button);
  element.appendChild(col_zero);

  if(mailbox === "inbox"){

    var button_send = document.createElement('input'),
    br_send = document.createElement('br');

    button_send.type  = 'button';
    button_send.value = "reply";
    button_send.className = "aux-button";
    button_send.addEventListener('click', () => {
      compose_email(email_now);
    });

    col_zero.appendChild(button_send);
    col_zero.appendChild(br_send);
    
  }

  let col_one = document.createElement('div');
  col_one.className = 'column';
  col_one.id = 'one-col-read';

  let subject = document.createElement("h3");
  subject.textContent = email_now.subject;

  col_one.appendChild(subject);
  element.appendChild(col_one);
  
  document.querySelector('#emails-view').append(element);

  if(mailbox === "inbox"){
    let sender = document.createElement("div");
    sender.className = 'row';
    sender.textContent = email_now.sender;
    document.querySelector('#emails-view').append(sender);
  } else{
    let recipient = document.createElement("div");
    recipient.className = 'row';
    recipient.textContent = "";

    for (let i = 0; i < email_now.recipients.length; i++) {
      recipient.textContent = recipient.textContent + email_now.recipients[i];
      if(email_now.recipients.length > 1){
        recipient.textContent = recipient.textContent  + ", ";
      }
    }
    document.querySelector('#emails-view').append(recipient);
  }

  
  let email_body = document.createElement("p");
  email_body.textContent = email_now.body;
  document.querySelector('#emails-view').append(email_body);
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if(mailbox === 'sent'){
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      show_emails(mailbox, emails);
      
    });
  } else if(mailbox == 'inbox'){
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      show_emails(mailbox, emails);
    });
  } else {
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      show_emails(mailbox, emails);
    });
  }

  return false;
}