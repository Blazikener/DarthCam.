// static/js/auth.js
let video = document.getElementById('webcam');

if (video) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => {
      alert('Webcam access denied or not available');
      console.error(err);
    });
}

function captureImage() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg');
}

function handleSignup() {
  const image = captureImage();
  const payload = {
    firstName: document.getElementById('firstName').value,
    lastName: document.getElementById('lastName').value,
    email: document.getElementById('email').value,
    username: document.getElementById('username').value,
    image: image
  };

  fetch('/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => alert(data.message))
  .catch(err => {
    console.error(err);
    alert('Error during signup.');
  });
}

function handleLogin() {
  const image = captureImage();
  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image })
  })
  .then(res => res.json())
  .then(data => alert(data.message || "Login Successful"))
  .catch(err => {
    console.error(err);
    alert('Error during login.');
  });
}

function toggleDropdown() {
  const dropdownMenu = document.getElementById('dropdownMenu');
  if (dropdownMenu) {
    dropdownMenu.style.display = dropdownMenu.style.display === 'flex' ? 'none' : 'flex';
  }
}
