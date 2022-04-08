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

  /* Create three equal columns that floats next to each other */
  .column {
    display: flex;
    align-items: center;
    width: 33.33%;
    padding: 10px;
    height: 75px;
    overflow: hidden;
    white-space: nowrap;
    
  }

  /* Clear floats after the columns */
  .row:after {
    content: "";
    display: table;
    clear: both;
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
    element.addEventListener('click', ()=> view_email(mailbox, email_now));
    
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

  let subject = document.createElement("h1");
  subject.textContent = email_now.subject;

  element.appendChild(subject);

  if(mailbox === "inbox"){
    let sender = document.createElement("p");
    sender.textContent = email_now.sender;
    element.appendChild(sender);
  } else{
    let recipient = document.createElement("p");
    recipient.textContent = "";
    for (let i = 0; i < email_now.recipients.length; i++) {
      recipient.textContent = recipient.textContent + email_now.recipients[i];
      if(email_now.recipients.length > 1){
        recipient.textContent = recipient.textContent  + ", ";
      }
    }
    element.appendChild(recipient);
  }

  var button = document.createElement('input'),
    archive = "archive";

    if(email_now.archived === true){
      archive = "unarchive";
    } 

  button.type  = 'button';
  button.value = archive;
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
        load_mailbox("inbox")
      });
  });

  element.appendChild(button);

  if(mailbox === "inbox"){

    var button_send = document.createElement('input'),
    br_send = document.createElement('br');

    button_send.type  = 'button';
    button_send.value = "reply";
    button_send.addEventListener('click', () => {
      compose_email(email_now);
    });

    element.appendChild(button_send);
    element.appendChild(br_send);
  }

  

  let email_body = document.createElement("p");
  email_body.textContent = email_now.body;
  element.appendChild(email_body);
  document.querySelector('#emails-view').append(element);
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