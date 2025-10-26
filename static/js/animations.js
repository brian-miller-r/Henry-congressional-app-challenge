/**
 * Advanced Animation System for Study Streak Motivator
 * Phase 7 - UI Polish and Animations
 * Congressional App Challenge 2025
 */

class AnimationEngine {
    constructor() {
        this.observers = [];
        this.celebratedBadges = new Set(); // Track which badges have been celebrated
        this.init();
    }

    init() {
        this.setupScrollAnimations();
        this.setupHoverEffects();
        this.setupCounters();
        this.setupPageTransitions();
        this.setupBadgeAnimations();
    }

    // Intersection Observer for scroll-triggered animations
    setupScrollAnimations() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '50px'
            });

            // Observe elements with animation classes
            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });

            this.observers.push(observer);
        }
    }

    // Enhanced hover effects for interactive elements
    setupHoverEffects() {
        // Card hover effects
        document.querySelectorAll('.placeholder-card, .stat-card, .chart-card').forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                e.target.classList.add('hover-active');
                this.createRippleEffect(e);
            });

            card.addEventListener('mouseleave', (e) => {
                e.target.classList.remove('hover-active');
            });
        });

        // Button enhanced effects
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.createButtonRipple(e);
            });
        });
    }

    // Animated counters for statistics
    setupCounters() {
        const counters = document.querySelectorAll('.animated-counter');
        
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target) || parseInt(counter.textContent);
            if (target) {
                this.animateCounter(counter, target);
            }
        });
    }

    animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16); // 60fps
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format numbers appropriately
            if (target > 1000) {
                element.textContent = Math.floor(current).toLocaleString();
            } else if (target % 1 !== 0) {
                element.textContent = current.toFixed(1);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }

    // Page transition effects
    setupPageTransitions() {
        // Add loading state for navigation
        document.querySelectorAll('a[href^="/"]').forEach(link => {
            link.addEventListener('click', (e) => {
                if (!e.ctrlKey && !e.metaKey) {
                    this.showPageTransition();
                }
            });
        });
    }

    showPageTransition() {
        const overlay = document.createElement('div');
        overlay.className = 'page-transition-overlay';
        document.body.appendChild(overlay);

        // Remove after animation
        setTimeout(() => {
            if (document.body.contains(overlay)) {
                document.body.removeChild(overlay);
            }
        }, 1000);
    }

    // Badge unlock celebration animations
    setupBadgeAnimations() {
        // Only set up event listeners, don't auto-celebrate on page load
        const badges = document.querySelectorAll('[data-badge-earned="true"]');
        badges.forEach((badge) => {
            // Add click event for manual celebration
            badge.addEventListener('click', () => {
                this.celebrateBadge(badge);
            });
        });
    }

    celebrateBadge(badgeElement) {
        // Create celebration overlay
        const celebration = document.createElement('div');
        celebration.className = 'badge-celebration';
        celebration.innerHTML = `
            <div class="celebration-content">
                <div class="celebration-badge">
                    ${badgeElement.querySelector('.badge-icon')?.textContent || '🏆'}
                </div>
                <div class="celebration-text">
                    <h3>Badge Earned!</h3>
                    <p>${badgeElement.dataset.badgeName || 'Achievement Unlocked'}</p>
                </div>
                <div class="celebration-particles"></div>
            </div>
        `;

        document.body.appendChild(celebration);

        // Create particle effects
        this.createParticles(celebration.querySelector('.celebration-particles'));

        // Auto-remove after animation
        setTimeout(() => {
            celebration.classList.add('fade-out');
            setTimeout(() => {
                if (document.body.contains(celebration)) {
                    document.body.removeChild(celebration);
                }
            }, 500);
        }, 3000);
    }

    createParticles(container) {
        const colors = ['#4285f4', '#34a853', '#fbbc05', '#ea4335', '#9c27b0'];
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 8 + 4}px;
                height: ${Math.random() * 8 + 4}px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                animation: particle-${Math.random() > 0.5 ? 'float' : 'burst'} ${Math.random() * 2 + 1}s ease-out forwards;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            container.appendChild(particle);
        }
    }

    createRippleEffect(event) {
        const button = event.currentTarget;
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        const ripple = document.createElement('div');
        ripple.className = 'ripple-effect';
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;

        // Ensure button has relative positioning
        if (getComputedStyle(button).position === 'static') {
            button.style.position = 'relative';
        }

        button.appendChild(ripple);

        // Remove ripple after animation
        setTimeout(() => {
            if (button.contains(ripple)) {
                button.removeChild(ripple);
            }
        }, 600);
    }

    createButtonRipple(event) {
        const button = event.currentTarget;
        button.classList.add('btn-clicked');
        
        setTimeout(() => {
            button.classList.remove('btn-clicked');
        }, 300);
    }

    // Progress bar animations
    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill, .progress-bar-circle');
        
        progressBars.forEach(bar => {
            const progress = bar.dataset.progress || bar.style.width;
            if (progress) {
                bar.style.transition = 'all 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
                
                // Trigger animation
                setTimeout(() => {
                    if (bar.classList.contains('progress-fill')) {
                        bar.style.width = progress;
                    } else if (bar.classList.contains('progress-bar-circle')) {
                        const circumference = 2 * Math.PI * 45;
                        const offset = circumference - (parseInt(progress) / 100) * circumference;
                        bar.style.strokeDashoffset = offset;
                    }
                }, 100);
            }
        });
    }

    // Chart entrance animations
    animateCharts() {
        // Animate chart.js charts if they exist
        if (window.Chart) {
            Chart.defaults.animation = {
                duration: 2000,
                easing: 'easeInOutCubic'
            };
        }

        // Animate custom chart elements
        document.querySelectorAll('.chart-element').forEach((element, index) => {
            element.style.animationDelay = `${index * 0.1}s`;
            element.classList.add('chart-animate-in');
        });
    }

    // Loading skeleton animations
    createSkeletonLoader(container) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-loader';
        skeleton.innerHTML = `
            <div class="skeleton-line skeleton-title"></div>
            <div class="skeleton-line skeleton-subtitle"></div>
            <div class="skeleton-line skeleton-content"></div>
            <div class="skeleton-line skeleton-content short"></div>
        `;
        
        container.innerHTML = '';
        container.appendChild(skeleton);
        
        return skeleton;
    }

    // Notification animations
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
                <span class="notification-message">${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('notification-show'), 100);

        // Auto-remove
        setTimeout(() => {
            notification.classList.remove('notification-show');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    // Cleanup observers
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers = [];
    }
}

// Initialize animation engine when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.animationEngine = new AnimationEngine();
    
    // Animate elements that are already visible
    setTimeout(() => {
        if (window.animationEngine) {
            window.animationEngine.animateProgressBars();
            window.animationEngine.animateCharts();
        }
    }, 500);
});

// Badge celebration helper for server responses (only for NEW badges)
window.celebrateNewBadge = function(badgeName, badgeIcon) {
    if (window.animationEngine) {
        const tempBadge = document.createElement('div');
        tempBadge.dataset.badgeName = badgeName;
        tempBadge.innerHTML = `<span class="badge-icon">${badgeIcon}</span>`;
        window.animationEngine.celebrateBadge(tempBadge);
        
        // Mark this badge as celebrated to avoid repeating
        window.animationEngine.celebratedBadges.add(badgeName);
    }
};

// Function to celebrate multiple new badges from API response
window.celebrateNewBadges = function(newBadges) {
    if (window.animationEngine && newBadges && newBadges.length > 0) {
        newBadges.forEach((badge, index) => {
            setTimeout(() => {
                window.celebrateNewBadge(badge.name, badge.icon);
            }, index * 1000); // Stagger multiple badge celebrations
        });
    }
};

// Notification helper
window.showNotification = function(message, type = 'success') {
    if (window.animationEngine) {
        window.animationEngine.showNotification(message, type);
    }
};