// Smooth scrolling of links in the menu
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        if (this.hash !== "") {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            } else {
                window.location.href = this.href;
            }
        }
    });
});

// Debug: check if JS is working
console.log("JavaScript działa! :)");