// Contact Form Validation
document.getElementById('contactForm').addEventListener('submit', function(event) {
  let name = document.getElementById('name').value;
  let email = document.getElementById('email').value;
  let message = document.getElementById('message').value;

  if (name === "" || email === "" || message === "") {
    alert("All fields must be filled out.");
    event.preventDefault();
  } else {
    alert("Thank you for your message!");
  }
});
