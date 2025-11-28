/*
* Initializes the theme toggle functionality.
* Checks for a saved theme in localStorage and applies it.
* Adds a click listener to the theme toggle button.
*/
function initThemeToggle() {
    const toggleButton = document.getElementById('theme-toggle');
    if (!toggleButton)
        return;

    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'light')
        document.body.classList.add('light-mode');

    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('light-mode');
        let theme = 'dark';
        if (document.body.classList.contains('light-mode'))
            theme = 'light';
        
        localStorage.setItem('theme', theme);
    });
}

/*
* Starts a countdown timer that redirects to the homepage.
*/
function startCountdown(seconds) {
    const countdownElement = document.getElementById('countdown');
    if (!countdownElement)
        return;

    countdownElement.textContent = seconds;
            
    const interval = setInterval(function() {
        seconds--;
        countdownElement.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(interval);
            window.location.href = "/";
        }
    }, 1000);
}

/*
* Initialize functionalities on DOMContentLoaded
*/
document.addEventListener('DOMContentLoaded', function() {
    initThemeToggle();
    if (document.getElementById('countdown')) {
        startCountdown(5);
    }
});