const form = document.querySelector("form");
const Name = document.getElementById("name");
const email = document.getElementById("email");
const Subject = document.getElementById("subject");
const Mess = document.getElementById("message");

function sendEmail() {
  const bodyMessage = `Name: ${Name.value}<br> Email: ${email.value}<br> Message: ${Mess.value}`;

  Email.send({
    Host: "smtp.elasticemail.com",
    Username: "strokeproject91@gmail.com",
    Password: "499CFD6AD5F5B3C1E03BA5652071B951D7D5",
    To: "strokeproject91@gmail.com",
    From: "strokeproject91@gmail.com",
    Subject: Subject.value,
    Body: bodyMessage,
  }).then((message) => {
    if (message == "OK") {
      Swal.fire({
        title: "Success!",
        text: "Message sent successfully!",
        icon: "success",
      }).then(() => {
        window.location.href = "/";
      });
    }
  });
}

form.addEventListener("submit", (e) => {
  e.preventDefault();

  sendEmail();
});
