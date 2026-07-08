document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide toasts after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 5000);
    });

    // Search toggle
    const searchToggles = document.querySelectorAll('#search-toggle, #search-toggle-mobile');
    const searchOverlay = document.getElementById('search-overlay');

    if (searchToggles.length > 0 && searchOverlay) {
        searchToggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                searchOverlay.classList.add('active');
                // Focus the search input when opened
                const searchInput = searchOverlay.querySelector('.search-input');
                if (searchInput) {
                    setTimeout(() => searchInput.focus(), 100);
                }
            });
        });

        searchOverlay.addEventListener('click', (e) => {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchOverlay.classList.remove('active');
            }
        });
    }

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuClose = document.getElementById('mobile-menu-close');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        if (mobileMenuClose) {
            mobileMenuClose.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        mobileMenu.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // Favorite button toggle
    const favoriteForms = document.querySelectorAll('.favorite-form');
    favoriteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const btn = this.querySelector('.product-fav-btn');
            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_favorited) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }

                // Update cart badge if needed
                if (data.cart_count !== undefined) {
                    const cartBadge = document.querySelector('.cart-badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                        if (data.cart_count === 0) {
                            cartBadge.style.display = 'none';
                        } else {
                            cartBadge.style.display = 'flex';
                        }
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Add to cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const btn = this.querySelector('button');
            const originalText = btn.textContent;

            btn.disabled = true;
            btn.textContent = 'Добавление...';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart badge
                    const cartBadge = document.querySelector('.cart-badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                        if (data.cart_count === 0) {
                            cartBadge.style.display = 'none';
                        } else {
                            cartBadge.style.display = 'flex';
                        }
                    }

                    // Show toast notification
                    showToast(data.message || 'Товар добавлен в корзину');

                    // Animate button
                    btn.textContent = '✓ Добавлено';
                    btn.style.background = '#10b981';

                    setTimeout(() => {
                        btn.disabled = false;
                        btn.textContent = originalText;
                        btn.style.background = '';
                    }, 2000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btn.disabled = false;
                btn.textContent = originalText;
            });
        });
    });

    // Toast notification function
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Auth card toggle
    const showRegisterBtn = document.getElementById('show-register');
    const showLoginBtn = document.getElementById('show-login');
    const loginCard = document.getElementById('login-card');
    const registerCard = document.getElementById('register-card');

    if (showRegisterBtn && registerCard && loginCard) {
        showRegisterBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loginCard.style.display = 'none';
            registerCard.style.display = 'block';
        });
    }

    if (showLoginBtn && registerCard && loginCard) {
        showLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            registerCard.style.display = 'none';
            loginCard.style.display = 'block';
        });
    }

    // Account navigation
    const accountNavItems = document.querySelectorAll('.account-nav-item[href^="#"]');
    const accountSections = document.querySelectorAll('.account-section');

    accountNavItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);

            // Update active nav item
            accountNavItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');

            // Show target section
            accountSections.forEach(section => {
                section.style.display = 'none';
                if (section.id === targetId) {
                    section.style.display = 'block';
                }
            });
        });
    });

    // Review modal functions
    window.openReviewModal = function(orderId) {
        const modal = document.getElementById('review-modal');
        const orderIdInput = document.getElementById('review-order-id');
        if (modal && orderIdInput) {
            orderIdInput.value = orderId;
            modal.style.display = 'flex';
        }
    };

    window.closeReviewModal = function() {
        const modal = document.getElementById('review-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    };

    // Close modal on outside click
    const reviewModal = document.getElementById('review-modal');
    if (reviewModal) {
        reviewModal.addEventListener('click', function(e) {
            if (e.target === reviewModal) {
                closeReviewModal();
            }
        });
    }

    // Reviews slider
    const reviewCards = document.querySelectorAll('.review-card');
    const reviewPrev = document.querySelector('.review-prev');
    const reviewNext = document.querySelector('.review-next');
    const reviewDots = document.getElementById('review-dots');

    if (reviewCards.length > 0 && reviewDots) {
        let currentReview = 0;

        // Create dots
        reviewCards.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.className = 'review-dot' + (index === 0 ? ' active' : '');
            dot.addEventListener('click', () => showReview(index));
            reviewDots.appendChild(dot);
        });

        function showReview(index) {
            reviewCards.forEach(card => card.classList.remove('active'));
            const dots = reviewDots.querySelectorAll('.review-dot');
            dots.forEach(dot => dot.classList.remove('active'));

            reviewCards[index].classList.add('active');
            dots[index].classList.add('active');
            currentReview = index;
        }

        if (reviewPrev) {
            reviewPrev.addEventListener('click', () => {
                currentReview = (currentReview - 1 + reviewCards.length) % reviewCards.length;
                showReview(currentReview);
            });
        }

        if (reviewNext) {
            reviewNext.addEventListener('click', () => {
                currentReview = (currentReview + 1) % reviewCards.length;
                showReview(currentReview);
            });
        }

        // Auto-rotate reviews
        setInterval(() => {
            currentReview = (currentReview + 1) % reviewCards.length;
            showReview(currentReview);
        }, 5000);
    }
});
