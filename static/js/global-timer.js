/**
 * Global Timer System - Works across all pages
 * Study Streak Motivator - Congressional App Challenge 2025
 */

class GlobalTimer {
    constructor() {
        this.storageKey = 'studyTimer';
        this.isTimerPage = window.location.pathname === '/timer';
        this.timerWidget = null;
        this.intervalId = null;
        
        this.init();
    }
    
    init() {
        // Load timer state from localStorage
        this.loadTimerState();
        
        // If timer is running and we're not on timer page, show widget
        if (this.isRunning() && !this.isTimerPage) {
            this.createTimerWidget();
            this.startWidgetUpdates();
        }
        
        // Listen for timer events from timer page
        window.addEventListener('storage', (e) => {
            if (e.key === this.storageKey) {
                this.handleTimerStateChange();
            }
        });
    }
    
    loadTimerState() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            this.timerData = JSON.parse(saved);
        } else {
            this.timerData = {
                isRunning: false,
                isPaused: false,
                timeRemaining: 0,
                totalTime: 0,
                subject: 'Math',
                sessionId: null,
                startTime: null
            };
        }
    }
    
    saveTimerState() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.timerData));
        // Trigger storage event for other tabs/pages
        window.dispatchEvent(new StorageEvent('storage', {
            key: this.storageKey,
            newValue: JSON.stringify(this.timerData)
        }));
    }
    
    isRunning() {
        return this.timerData.isRunning && !this.timerData.isPaused;
    }
    
    startTimer(duration, subject, sessionId) {
        this.timerData = {
            isRunning: true,
            isPaused: false,
            timeRemaining: duration * 60,
            totalTime: duration * 60,
            subject: subject,
            sessionId: sessionId,
            startTime: Date.now()
        };
        this.saveTimerState();
        
        if (!this.isTimerPage) {
            this.createTimerWidget();
            this.startWidgetUpdates();
        }
    }
    
    pauseTimer() {
        this.timerData.isPaused = true;
        this.saveTimerState();
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        this.updateWidget();
    }
    
    resumeTimer() {
        this.timerData.isPaused = false;
        this.saveTimerState();
        
        if (!this.isTimerPage) {
            this.startWidgetUpdates();
        }
    }
    
    stopTimer() {
        this.timerData.isRunning = false;
        this.timerData.isPaused = false;
        this.saveTimerState();
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        this.removeTimerWidget();
    }
    
    tick() {
        if (!this.isRunning()) return;
        
        // Only calculate time if we're not on the timer page 
        // (timer page handles its own countdown)
        if (!this.isTimerPage) {
            const elapsed = Math.floor((Date.now() - this.timerData.startTime) / 1000);
            this.timerData.timeRemaining = Math.max(0, this.timerData.totalTime - elapsed);
        }
        
        if (this.timerData.timeRemaining <= 0) {
            // Timer completed
            this.completeTimer();
            return;
        }
        
        if (!this.isTimerPage) {
            this.saveTimerState();
        }
        this.updateWidget();
    }
    
    completeTimer() {
        // Timer completed naturally
        this.stopTimer();
        this.showCompletionNotification();
    }
    
    createTimerWidget() {
        if (this.timerWidget || this.isTimerPage) return;
        
        this.timerWidget = document.createElement('div');
        this.timerWidget.className = 'global-timer-widget';
        this.timerWidget.innerHTML = `
            <div class="timer-widget-content">
                <div class="timer-widget-time">25:00</div>
                <div class="timer-widget-subject">Math</div>
                <div class="timer-widget-controls">
                    <button id="widget-pause" class="timer-widget-btn">⏸️</button>
                    <button id="widget-resume" class="timer-widget-btn" style="display: none;">▶️</button>
                    <button id="widget-stop" class="timer-widget-btn">⏹️</button>
                    <a href="/timer" class="timer-widget-btn">🔍</a>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.timerWidget);
        
        // Add event listeners
        const pauseBtn = this.timerWidget.querySelector('#widget-pause');
        const resumeBtn = this.timerWidget.querySelector('#widget-resume');
        const stopBtn = this.timerWidget.querySelector('#widget-stop');
        
        pauseBtn.addEventListener('click', () => this.pauseTimer());
        resumeBtn.addEventListener('click', () => this.resumeTimer());
        stopBtn.addEventListener('click', () => {
            if (confirm('Stop the current study session?')) {
                this.stopTimer();
            }
        });
        
        this.updateWidget();
    }
    
    updateWidget() {
        if (!this.timerWidget) return;
        
        const minutes = Math.floor(this.timerData.timeRemaining / 60);
        const seconds = this.timerData.timeRemaining % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const timeEl = this.timerWidget.querySelector('.timer-widget-time');
        const subjectEl = this.timerWidget.querySelector('.timer-widget-subject');
        const pauseBtn = this.timerWidget.querySelector('#widget-pause');
        const resumeBtn = this.timerWidget.querySelector('#widget-resume');
        
        if (timeEl) timeEl.textContent = timeString;
        if (subjectEl) subjectEl.textContent = this.timerData.subject;
        
        // Update button visibility based on pause state
        if (this.timerData.isPaused) {
            pauseBtn.style.display = 'none';
            resumeBtn.style.display = 'inline-block';
        } else {
            pauseBtn.style.display = 'inline-block';
            resumeBtn.style.display = 'none';
        }
        
        // Update widget color based on time remaining
        const progress = 1 - (this.timerData.timeRemaining / this.timerData.totalTime);
        if (progress > 0.8) {
            this.timerWidget.classList.add('timer-widget-urgent');
        } else {
            this.timerWidget.classList.remove('timer-widget-urgent');
        }
    }
    
    removeTimerWidget() {
        if (this.timerWidget) {
            this.timerWidget.remove();
            this.timerWidget = null;
        }
    }
    
    startWidgetUpdates() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
        
        this.intervalId = setInterval(() => {
            this.tick();
        }, 1000);
    }
    
    handleTimerStateChange() {
        this.loadTimerState();
        
        if (this.isRunning() && !this.isTimerPage) {
            if (!this.timerWidget) {
                this.createTimerWidget();
            }
            if (!this.intervalId) {
                this.startWidgetUpdates();
            }
            this.updateWidget();
        } else if (!this.isRunning()) {
            this.removeTimerWidget();
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        } else if (this.timerData.isPaused) {
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
            this.updateWidget();
        }
    }
    
    showCompletionNotification() {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Study Session Complete!', {
                body: `Great job! You completed your ${this.timerData.subject} session.`,
                icon: '/static/img/icon-192x192.png' // Add app icon if available
            });
        }
        
        // Show in-page notification
        const notification = document.createElement('div');
        notification.className = 'timer-completion-notification';
        notification.innerHTML = `
            <div class="completion-content">
                <h3>🎉 Session Complete!</h3>
                <p>Great job on your ${this.timerData.subject} session!</p>
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // Method for timer page to sync with global state
    syncWithTimerPage(timerInstance) {
        if (!this.isTimerPage) return;
        
        // Update timer page when global state changes
        window.addEventListener('storage', (e) => {
            if (e.key === this.storageKey && timerInstance) {
                const newState = JSON.parse(e.newValue);
                // Update timer page display without disrupting local timer
                if (!timerInstance.isRunning && newState.isRunning) {
                    // Timer was started from another page - sync state
                    timerInstance.timeRemaining = newState.timeRemaining;
                    timerInstance.selectedSubject = newState.subject;
                    timerInstance.sessionId = newState.sessionId;
                    timerInstance.isRunning = newState.isRunning;
                    timerInstance.isPaused = newState.isPaused;
                    timerInstance.updateDisplay();
                    timerInstance.updateButtonStates();
                }
            }
        });
    }
    
    // Request notification permission
    static requestNotificationPermission() {
        if ('Notification' in window && Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }
}

// Initialize global timer system
const globalTimer = new GlobalTimer();

// Request notification permission on first load
GlobalTimer.requestNotificationPermission();

// Export for use by timer page
window.globalTimer = globalTimer;