// Cart JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeCart();
    initializeCheckout();
    initializeAnimations();
});

function initializeCart() {
    // Initialize quantity controls
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.closest('.cart-item').dataset.itemId;
            const newQuantity = parseInt(this.value);
            updateCartItemQuantity(itemId, newQuantity);
        });
        
        // Prevent invalid input
        input.addEventListener('input', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 999;
            let value = parseInt(this.value);
            
            if (isNaN(value) || value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
    
    // Initialize remove buttons
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.closest('.cart-item').dataset.itemId;
            showRemoveConfirmation(itemId);
        });
    });
    
    // Initialize coupon form
    const couponForm = document.querySelector('.coupon-form');
    if (couponForm) {
        couponForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyCouponCode();
        });
    }
    
    // Auto-save cart state
    startAutoSave();
}

function initializeCheckout() {
    const checkoutForm = document.getElementById('checkout-form');
    if (!checkoutForm) return;
    
    // Initialize form validation
    const requiredFields = checkoutForm.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            validateField(this);
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });
    
    // Initialize payment method selection
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            updatePaymentMethodUI(this.value);
        });
    });
    
    // Initialize address copying
    const sameAsShippingCheckbox = document.querySelector('input[name="same_as_shipping"]');
    if (sameAsShippingCheckbox) {
        sameAsShippingCheckbox.addEventListener('change', function() {
            if (this.checked) {
                copyShippingToBilling();
            }
        });
    }
    
    // Initialize card number formatting
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function() {
            formatCardNumber(this);
        });
    }
    
    // Initialize expiry date formatting
    const cardExpiryInput = document.getElementById('card_expiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', function() {
            formatExpiryDate(this);
        });
    }
}

function initializeAnimations() {
    // Animate cart items on load
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.6s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Animate summary on scroll
    const cartSummary = document.querySelector('.cart-summary');
    if (cartSummary) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            cartSummary.style.transform = `translateY(${rate}px)`;
        });
    }
}

// Cart Operations
function updateCartItemQuantity(itemId, quantity) {
    if (quantity < 1) {
        showRemoveConfirmation(itemId);
        return;
    }
    
    showLoadingState();
    
    fetch('/cart/update-quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingState();
        
        if (data.success) {
            updateCartUI(data);
            showNotification('Cart updated successfully!', 'success');
        } else {
            showNotification(data.message || 'Failed to update cart', 'error');
            revertQuantityInput(itemId);
        }
    })
    .catch(error => {
        hideLoadingState();
        showNotification('An error occurred. Please try again.', 'error');
        revertQuantityInput(itemId);
    });
}

function removeCartItem(itemId) {
    showLoadingState();
    
    fetch('/cart/remove-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingState();
        
        if (data.success) {
            removeCartItemFromUI(itemId);
            updateCartSummary(data.cart_summary);
            showNotification('Item removed from cart', 'success');
            
            // Redirect to empty cart page if no items left
            if (data.cart_summary.total_items === 0) {
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
        } else {
            showNotification(data.message || 'Failed to remove item', 'error');
        }
    })
    .catch(error => {
        hideLoadingState();
        showNotification('An error occurred. Please try again.', 'error');
    });
}

function applyCouponCode() {
    const couponInput = document.querySelector('.coupon-input');
    const couponCode = couponInput.value.trim();
    
    if (!couponCode) {
        showNotification('Please enter a coupon code', 'error');
        return;
    }
    
    showLoadingState();
    
    fetch('/cart/apply-coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            coupon_code: couponCode
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingState();
        
        if (data.success) {
            updateCartSummary(data.cart_summary);
            showNotification(data.message, 'success');
            couponInput.value = '';
        } else {
            showNotification(data.message || 'Invalid coupon code', 'error');
        }
    })
    .catch(error => {
        hideLoadingState();
        showNotification('An error occurred. Please try again.', 'error');
    });
}

// UI Updates
function updateCartUI(data) {
    // Update item total
    const itemElement = document.querySelector(`[data-item-id="${data.item_id}"]`);
    if (itemElement) {
        const totalElement = itemElement.querySelector('.item-total');
        if (totalElement) {
            totalElement.textContent = `$${data.item_total}`;
        }
    }
    
    // Update cart summary
    updateCartSummary(data.cart_summary);
    
    // Update cart count in header
    updateCartCount(data.cart_summary.total_items);
}

function updateCartSummary(summary) {
    const elements = {
        subtotal: document.querySelector('.cart-subtotal'),
        shipping: document.querySelector('.cart-shipping'),
        tax: document.querySelector('.cart-tax'),
        discount: document.querySelector('.cart-discount'),
        total: document.querySelector('.cart-total')
    };
    
    if (elements.subtotal) elements.subtotal.textContent = `$${summary.subtotal}`;
    if (elements.shipping) elements.shipping.textContent = `$${summary.shipping}`;
    if (elements.tax) elements.tax.textContent = `$${summary.tax}`;
    if (elements.discount) elements.discount.textContent = `-$${summary.discount}`;
    if (elements.total) elements.total.textContent = `$${summary.total}`;
    
    // Update item count
    const itemCountElements = document.querySelectorAll('.cart-item-count');
    itemCountElements.forEach(element => {
        element.textContent = summary.total_items;
    });
}

function removeCartItemFromUI(itemId) {
    const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
    if (itemElement) {
        itemElement.style.transition = 'all 0.5s ease';
        itemElement.style.opacity = '0';
        itemElement.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            itemElement.remove();
        }, 500);
    }
}

function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
        
        // Add bounce animation
        element.style.transform = 'scale(1.2)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    });
}

// Form Validation
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Remove existing validation classes
    field.classList.remove('error', 'success');
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required';
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }
    }
    
    // Phone validation
    if (field.type === 'tel' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            isValid = false;
            message = 'Please enter a valid phone number';
        }
    }
    
    // Card number validation
    if (field.name === 'card_number' && value) {
        const cardRegex = /^[\d\s]{13,19}$/;
        if (!cardRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid card number';
        }
    }
    
    // Expiry date validation
    if (field.name === 'card_expiry' && value) {
        const expiryRegex = /^(0[1-9]|1[0-2])\/\d{2}$/;
        if (!expiryRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid expiry date (MM/YY)';
        }
    }
    
    // CVC validation
    if (field.name === 'card_cvc' && value) {
        const cvcRegex = /^\d{3,4}$/;
        if (!cvcRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid CVC';
        }
    }
    
    // Apply validation result
    if (isValid) {
        field.classList.add('success');
        removeFieldError(field);
    } else {
        field.classList.add('error');
        showFieldError(field, message);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    removeFieldError(field);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error text-red-600 text-sm mt-1';
    errorElement.textContent = message;
    
    field.parentNode.appendChild(errorElement);
}

function removeFieldError(field) {
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

// Form Formatting
function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    
    if (formattedValue.length > 19) {
        formattedValue = formattedValue.substring(0, 19);
    }
    
    input.value = formattedValue;
}

function formatExpiryDate(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    
    input.value = value;
}

function copyShippingToBilling() {
    const shippingFields = {
        name: document.getElementById('shipping_name'),
        email: document.getElementById('shipping_email'),
        address: document.getElementById('shipping_address'),
        city: document.getElementById('shipping_city'),
        state: document.getElementById('shipping_state'),
        postal_code: document.getElementById('shipping_postal_code'),
        country: document.getElementById('shipping_country')
    };
    
    const billingFields = {
        name: document.getElementById('billing_name'),
        email: document.getElementById('billing_email'),
        address: document.getElementById('billing_address'),
        city: document.getElementById('billing_city'),
        state: document.getElementById('billing_state'),
        postal_code: document.getElementById('billing_postal_code'),
        country: document.getElementById('billing_country')
    };
    
    Object.keys(shippingFields).forEach(key => {
        if (shippingFields[key] && billingFields[key]) {
            billingFields[key].value = shippingFields[key].value;
        }
    });
}

function updatePaymentMethodUI(method) {
    // Update payment method selection UI
    const paymentSections = document.querySelectorAll('.payment-section');
    paymentSections.forEach(section => {
        section.style.display = 'none';
    });
    
    const selectedSection = document.querySelector(`.payment-section[data-method="${method}"]`);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

// Confirmation Modals
function showRemoveConfirmation(itemId) {
    const modal = document.getElementById('remove-confirmation-modal');
    if (modal) {
        modal.dataset.itemId = itemId;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        // Fallback to browser confirm
        if (confirm('Are you sure you want to remove this item from your cart?')) {
            removeCartItem(itemId);
        }
    }
}

function confirmRemoveItem() {
    const modal = document.getElementById('remove-confirmation-modal');
    const itemId = modal.dataset.itemId;
    
    if (itemId) {
        removeCartItem(itemId);
        closeRemoveConfirmation();
    }
}

function closeRemoveConfirmation() {
    const modal = document.getElementById('remove-confirmation-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        delete modal.dataset.itemId;
    }
}

// Loading States
function showLoadingState() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    } else {
        // Create loading overlay
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-spinner">
                <i class="fas fa-spinner fa-spin"></i>
                <div>Processing...</div>
            </div>
        `;
        document.body.appendChild(overlay);
    }
}

function hideLoadingState() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
}

// Auto-save
function startAutoSave() {
    // Save cart state periodically
    setInterval(() => {
        saveCartState();
    }, 30000); // Save every 30 seconds
    
    // Save on page unload
    window.addEventListener('beforeunload', saveCartState);
}

function saveCartState() {
    const cartData = {
        timestamp: Date.now(),
        items: []
    };
    
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach(item => {
        const itemId = item.dataset.itemId;
        const quantityInput = item.querySelector('.quantity-input');
        
        if (itemId && quantityInput) {
            cartData.items.push({
                id: itemId,
                quantity: parseInt(quantityInput.value)
            });
        }
    });
    
    localStorage.setItem('agromarket_cart', JSON.stringify(cartData));
}

function restoreCartState() {
    const savedCart = localStorage.getItem('agromarket_cart');
    if (savedCart) {
        try {
            const cartData = JSON.parse(savedCart);
            // Restore cart state if needed
            console.log('Restored cart state:', cartData);
        } catch (error) {
            console.error('Failed to restore cart state:', error);
        }
    }
}

// Utility Functions
function revertQuantityInput(itemId) {
    const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
    if (itemElement) {
        const quantityInput = itemElement.querySelector('.quantity-input');
        if (quantityInput) {
            // Revert to previous value (stored in data attribute)
            const previousValue = quantityInput.dataset.previousValue || quantityInput.min || 1;
            quantityInput.value = previousValue;
        }
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
window.AgroMarketCart = {
    updateCartItemQuantity,
    removeCartItem,
    applyCouponCode,
    showRemoveConfirmation,
    confirmRemoveItem,
    closeRemoveConfirmation
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    restoreCartState();
});