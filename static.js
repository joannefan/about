
function getNavHtml() {
    const html = 
    `<div class="navbar">
        <div class="logo"></div>
        <!-- <img src="images/logo.png" class="logo"> -->
        <div class="nav-links">
            <a href="index.html" class="btn draw-border">Home</a>
            <a href="about.html" class="btn draw-border">About</a>
            <a href="experience.html" class="btn draw-border">Experience</a>
        </div>
    </div>`;

    return html;
}

function getSidebarHtml(color) {
    const html = 
    `<img src="images/menu.png" class="menu">
    <div class="social-links">
        <a href="https://www.linkedin.com/in/joannefan/" target="_blank">
            <img src="images/linkedin_${color}.png" alt="LinkedIn logo">
        </a>
        <a href="https://github.com/joannefan/" target="_blank">
            <img src="images/github_${color}.png" alt="GitHub logo">
        </a>
    </div>`;

    return html;
}