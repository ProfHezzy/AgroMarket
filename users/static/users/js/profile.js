// Profile JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeProfile();
    initializeTabs();
    initializeImageUpload();
    initializeFormValidation();
    initializeAnimations();
});

function initializeProfile() {
    // Initialize profile interactions
    initializeFollowButton();
    initializeContactModal();
    initializeShareProfile();
    
    // Load user activity
    loadRecentActivity();
    
    // Initialize lazy loading for images
    initializeLazyLoading();
}

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding content
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
                
                // Animate content
                targetContent.style.opacity = '0';
                targetContent.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    targetContent.style.transition = 'all 0.3s ease';
                    targetContent.style.opacity = '1';
                    targetContent.style.transform = 'translateY(0)';
                }, 50);
            }
            
            // Update URL hash
            window.history.replaceState(null, null, `#${targetTab}`);
        });
    });
    
    // Initialize tab from URL hash
    const hash = window.location.hash.substring(1);
    if (hash) {
        const targetButton = document.querySelector(`[data-tab="${hash}"]`);
        if (targetButton) {
            targetButton.click();
        }
    }
}

function initializeImageUpload() {
    const imageInput = document.getElementById('profile_image');
    const imagePreview = document.getElementById('profile-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    showNotification('Please select a valid image file.', 'error');
                    return;
                }
                
                // Validate file size (5MB max)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('Image size must be less than 5MB.', 'error');
                    return;
                }
                
                // Preview image
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.innerHTML = `
                        <img src="${e.target.result}" 
                             alt="Profile Preview" 
                             class="w-32 h-32 rounded-full object-cover border-4 border-gray-200">
                    `;
                    
                    // Add upload animation
                    imagePreview.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        imagePreview.style.transition = 'transform 0.3s ease';
                        imagePreview.style.transform = 'scale(1)';
                    }, 100);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Drag and drop functionality
    const uploadArea = document.querySelector('.image-upload-container');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && imageInput) {
                imageInput.files = files;
                imageInput.dispatchEvent(new Event('change'));
            }
        });
    }
}

function initializeFormValidation() {
    const form = document.querySelector('.profile-edit-form form');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Please correct the errors in the form.', 'error');
        } else {
            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Saving...';
            }
        }
    });
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Remove existing validation classes
    field.classList.remove('error', 'success');
    removeFieldError(field);
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address.';
        }
    }
    
    // Username validation
    if (field.name === 'username' && value) {
        if (value.length < 3) {
            isValid = false;
            message = 'Username must be at least 3 characters long.';
        } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
            isValid = false;
            message = 'Username can only contain letters, numbers, and underscores.';
        }
    }
    
    // Phone number validation
    if (field.name === 'phone_number' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            isValid = false;
            message = 'Please enter a valid phone number.';
        }
    }
    
    // Apply validation result
    if (isValid) {
        field.classList.add('success');
    } else {
        field.classList.add('error');
        showFieldError(field, message);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    let errorElement = field.parentNode.querySelector('.field-error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error-message text-red-600 text-sm mt-1';
        field.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = message;
}

function removeFieldError(field) {
    const errorElement = field.parentNode.querySelector('.field-error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

function initializeAnimations() {
    // Animate profile elements on load
    const animatedElements = document.querySelectorAll('.stat-card, .profile-tabs, .contact-info, .business-info');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        
        observer.observe(element);
    });
    
    // Animate stats on scroll
    animateStatsOnScroll();
}

function animateStatsOnScroll() {
    const statValues = document.querySelectorAll('.stat-value');
    let animated = false;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                statValues.forEach((stat, index) => {
                    setTimeout(() => {
                        animateNumber(stat);
                    }, index * 200);
                });
            }
        });
    });
    
    if (statValues.length > 0) {
        observer.observe(statValues[0].closest('.profile-stats'));
    }
}

function animateNumber(element) {
    const finalValue = parseInt(element.textContent) || 0;
    const duration = 2000;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.floor(finalValue * easeOutQuart(progress));
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    element.textContent = '0';
    requestAnimationFrame(updateNumber);
}

function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
}

function initializeFollowButton() {
    const followButton = document.getElementById('follow-button');
    if (!followButton) return;
    
    followButton.addEventListener('click', function() {
        const isFollowing = this.classList.contains('following');
        const userId = this.dataset.userId;
        
        // Optimistic UI update
        if (isFollowing) {
            this.classList.remove('following');
            this.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Follow';
        } else {
            this.classList.add('following');
            this.innerHTML = '<i class="fas fa-user-check mr-2"></i>Following';
        }
        
        // API call
        fetch('/users/toggle-follow/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `user_id=${userId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
            } else {
                // Revert optimistic update
                if (isFollowing) {
                    this.classList.add('following');
                    this.innerHTML = '<i class="fas fa-user-check mr-2"></i>Following';
                } else {
                    this.classList.remove('following');
                    this.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Follow';
                }
                showNotification(data.message, 'error');
            }
        })
        .catch(error => {
            // Revert optimistic update
            if (isFollowing) {
                this.classList.add('following');
                this.innerHTML = '<i class="fas fa-user-check mr-2"></i>Following';
            } else {
                this.classList.remove('following');
                this.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Follow';
            }
            showNotification('An error occurred. Please try again.', 'error');
        });
    });
}

function initializeContactModal() {
    const contactButtons = document.querySelectorAll('.contact-user-btn');
    const contactModal = document.getElementById('contact-modal');
    const contactForm = document.getElementById('contact-form');
    
    contactButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (contactModal) {
                contactModal.classList.remove('hidden');
                contactModal.classList.add('flex');
            }
        });
    });
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendContactMessage();
        });
    }
    
    // Close modal handlers
    const closeButtons = document.querySelectorAll('.close-modal');
    closeButtons.forEach(button => {
        button.addEventListener('click', closeContactModal);
    });
    
    if (contactModal) {
        contactModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeContactModal();
            }
        });
    }
}

function sendContactMessage() {
    const form = document.getElementById('contact-form');
    const formData = new FormData(form);
    
    fetch('/users/send-message/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Message sent successfully!', 'success');
            closeContactModal();
            form.reset();
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        showNotification('An error occurred. Please try again.', 'error');
    });
}

function closeContactModal() {
    const contactModal = document.getElementById('contact-modal');
    if (contactModal) {
        contactModal.classList.add('hidden');
        contactModal.classList.remove('flex');
    }
}

function initializeShareProfile() {
    const shareButton = document.getElementById('share-profile');
    if (!shareButton) return;
    
    shareButton.addEventListener('click', function() {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                url: window.location.href
            });
        } else {
            navigator.clipboard.writeText(window.location.href).then(() => {
                showNotification('Profile link copied to clipboard!', 'success');
            });
        }
    });
}

function loadRecentActivity() {
    const activityContainer = document.getElementById('recent-activity');
    if (!activityContainer) return;
    
    // Simulate loading recent activity
    const activities = [
        { text: 'Updated profile information', time: '2 hours ago' },
        { text: 'Listed a new product', time: '1 day ago' },
        { text: 'Replied to a forum discussion', time: '2 days ago' },
        { text: 'Received a 5-star review', time: '3 days ago' },
        { text: 'Joined AgroMarket', time: '1 week ago' }
    ];
    
    const activityHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-dot"></div>
            <div class="activity-content">${activity.text}</div>
            <div class="activity-time">${activity.time}</div>
        </div>
    `).join('');
    
    activityContainer.innerHTML = activityHTML;
}

function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });
}

// Profile Actions
function editProfile() {
    window.location.href = '/users/profile/edit/';
}

function changePassword() {
    window.location.href = '/users/change-password/';
}

function viewProduct(productId) {
    window.location.href = `/marketplace/product/${productId}/`;
}

function viewThread(threadId) {
    window.location.href = `/forum/thread/${threadId}/`;
}

// Utility Functions
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
    // Use global notification system if available
    if (window.AgroMarket && window.AgroMarket.showNotification) {
        window.AgroMarket.showNotification(message, type);
    } else {
        // Fallback notification
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 ease-in-out translate-x-full`;
        
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                notification.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                notification.classList.add('bg-blue-500', 'text-white');
        }
        
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
    }
}

// Export functions for global use
window.ProfileManager = {
    editProfile,
    changePassword,
    viewProduct,
    viewThread,
    sendContactMessage,
    closeContactModal
};