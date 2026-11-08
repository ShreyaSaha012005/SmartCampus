// Add active class to current nav link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath && currentPath !== '/') {
            link.classList.add('active');
        } else if (currentPath === '/' && link.getAttribute('href') === '/') {
            link.classList.add('active');
        }
    });

    // Auto-hide flash messages after 3 seconds
    const flashMessages = document.querySelectorAll('.flash');
    if(flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transform = 'translateX(100%)';
                msg.style.transition = 'all 0.5s ease';
                setTimeout(() => msg.remove(), 500);
            });
        }, 3000);
    }
});
