// Forum Threads JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeThreads();
    initializeSearch();
    initializeModals();
});

function initializeThreads() {
    const threadItems = document.querySelectorAll('.thread-item');
    
    threadItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
        
        item.addEventListener('click', function(e) {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                const threadLink = this.querySelector('a[href*="thread"]');
                if (threadLink) {
                    window.location.href = threadLink.href;
                }
            }
        });
    });
}

function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        searchTimeout = setTimeout(() => {
            if (query.length >= 2) {
                performSearch(query);
            }
        }, 300);
    });
}

function performSearch(query) {
    // Implementation for search functionality
    console.log('Searching for:', query);
}

function initializeModals() {
    const newThreadModal = document.getElementById('new-thread-modal');
    
    if (newThreadModal) {
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && !newThreadModal.classList.contains('hidden')) {
                closeNewThreadModal();
            }
        });
        
        newThreadModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeNewThreadModal();
            }
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showNotification(message, type = 'info') {
    if (window.AgroMarket && window.AgroMarket.showNotification) {
        window.AgroMarket.showNotification(message, type);
    } else {
        alert(message);
    }
}