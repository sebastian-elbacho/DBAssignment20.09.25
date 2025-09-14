// Portfolio JavaScript
console.log('Portfolio loaded successfully!');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready!');
    
    // Add smooth scrolling to navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add smooth transition effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
        
        // Add hover effects
        link.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#555';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Add form validation if contact form exists
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const name = document.querySelector('input[name="name"]');
            const email = document.querySelector('input[name="email"]');
            
            if (name && name.value.trim() === '') {
                alert('Please enter your name');
                e.preventDefault();
                return false;
            }
            
            if (email && !email.value.includes('@')) {
                alert('Please enter a valid email');
                e.preventDefault();
                return false;
            }
            
            console.log('Form submitted successfully!');
        });
    }
});