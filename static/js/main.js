// Main JavaScript for Virginia Garden Planner

document.addEventListener('DOMContentLoaded', function() {
    // Enable all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle frost warnings
    const frostWarnings = document.querySelectorAll('.frost-warning');
    frostWarnings.forEach(warning => {
        warning.style.animation = 'pulse 2s infinite';
    });

    // Add pulse animation
    if (!document.querySelector('#pulseAnimation')) {
        const style = document.createElement('style');
        style.id = 'pulseAnimation';
        style.textContent = `
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.8; }
                100% { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    // Responsive image handling
    const vegImages = document.querySelectorAll('.card-img-top');
    vegImages.forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.jpg';
        });
    });

    // Weather refresh button handling
    const refreshWeather = document.querySelector('#refresh-weather');
    if (refreshWeather) {
        refreshWeather.addEventListener('click', function(e) {
            e.preventDefault();
            location.reload();
        });
    }

    // Task completion handling
    const taskItems = document.querySelectorAll('.list-group-item');
    taskItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('text-muted');
            this.style.textDecoration = this.classList.contains('text-muted') ? 'line-through' : 'none';
        });
    });

    // Mobile menu handling
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
});
