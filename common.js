// Common navbar JS for role separation
function getRole() {
  return localStorage.getItem('userRole');
}

function isLoggedIn() {
  return localStorage.getItem('userLoggedIn') === 'true';
}

function toggleMobileMenu() {
  const navMenu = document.getElementById('navMenu');
  const hamburger = document.getElementById('hamburger');
  
  if (navMenu.classList.contains('active')) {
    navMenu.classList.remove('active');
    hamburger.classList.remove('active');
  } else {
    navMenu.classList.add('active');
    hamburger.classList.add('active');
  }
}

// Close mobile menu when a link is clicked
document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      const navMenu = document.getElementById('navMenu');
      const hamburger = document.getElementById('hamburger');
      navMenu.classList.remove('active');
      hamburger.classList.remove('active');
    });
  });
});

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
  
  // Re-attach event listeners after updating
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      const navMenuEl = document.getElementById('navMenu');
      const hamburger = document.getElementById('hamburger');
      if (navMenuEl && hamburger) {
        navMenuEl.classList.remove('active');
        hamburger.classList.remove('active');
      }
    });
  });
}

function logout() {
  localStorage.clear();
  renderNavbar();
  alert('Logged out');
}

document.addEventListener('DOMContentLoaded', renderNavbar);
