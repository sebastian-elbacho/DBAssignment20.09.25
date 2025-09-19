
console.log('Portfolio loaded successfully!');


document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready!');
    
   
 const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
        
        
        link.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#555';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    
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


// Hamburger menu
const menu = document.querySelector('.hamburger'); 
const nav = document.getElementById('nav-menu');

if (menu && nav) {
    menu.addEventListener('click', () => { 
        menu.classList.toggle('hamburger--active'); 
        nav.classList.toggle('nav--open'); 
    });
}





