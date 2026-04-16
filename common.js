// Common navbar JS for role separation
function getRole() {
  return localStorage.getItem('userRole');
}

function isLoggedIn() {
  return localStorage.getItem('userLoggedIn') === 'true';
}

function renderNavbar() {
  const navMenu = document.querySelector('.nav-menu');
  if (!navMenu) return;

  const role = getRole();
  let html = `
    <li class="nav-item"><a href="index.html" class="nav-link">Home</a></li>
  `;

  if (isLoggedIn()) {
    if (role === 'student') {
      html += `
        <li class="nav-item"><a href="upload.html" class="nav-link">Upload</a></li>
        <li class="nav-item"><a href="my-uploads.html" class="nav-link">My Uploads</a></li>
        <li class="nav-item"><a href="#" class="nav-link" onclick="logout()">Logout</a></li>
      `;
    } else if (role === 'admin') {
      html += `
        <li class="nav-item"><a href="admin_new.html" class="nav-link">Dashboard</a></li>
        <li class="nav-item"><a href="#" class="nav-link" onclick="logout()">Logout</a></li>
      `;
    }
  } else {
    html += `
      <li class="nav-item portal-nav"><a href="student_login.html" class="nav-link">Student Portal</a></li>
      <li class="nav-item portal-nav"><a href="admin_login.html" class="nav-link">Admin Portal</a></li>
    `;
  }

  navMenu.innerHTML = html;
}

function logout() {
  localStorage.clear();
  renderNavbar();
  alert('Logged out');
}

document.addEventListener('DOMContentLoaded', renderNavbar);
