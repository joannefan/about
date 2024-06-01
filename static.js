
function getNavHtml() {
    const html = 
    `<nav>
      <ul>
        <li>
          <a href="index.html" class="btn draw-border">Home</a>
        </li>
        <li>
          <a href="about.html" class="btn draw-border">About</a>
        </li>
        <li>
          <a href="experience.html" class="btn draw-border">Experience</a>
        </li>
        <li>
          <a href="project.html" class="btn draw-border">Projects</a>
        </li>
        <li>
          <a href="https://github.com/joannefan" target="_blank" class="btn draw-border">GitHub</a>
        </li>
        <li class="hamburger">
          <a href="#">
            <div class="bar"></div>
          </a>
        </li>
      </ul>
    </nav>`;

    return html;
}

function getSidebarHtml(color) {
    const html = 
    `<div class="social-links">
        <a href="https://github.com/joannefan" target="_blank">
            <img src="images/linkedin_${color}.png" alt="LinkedIn logo">
        </a>
        <a href="https://github.com/joannefan/" target="_blank">
            <img src="images/github_${color}.png" alt="GitHub logo">
        </a>
    </div>`;

    return html;
}