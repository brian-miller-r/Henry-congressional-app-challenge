/**
 * Simple Working Timer - Phase 3
 * Study Streak Motivator - Congressional App Challenge 2025
 */

let timer = {
    timeRemaining: 1500, // 25 minutes in seconds
    isRunning: false,
    isPaused: false,
    intervalId: null,
    selectedDuration: 25,
    selectedSubject: 'Math',
    sessionId: null,

    init() {
        // Replace native alert with custom modal to avoid blocking dialogs
        const originalAlert = window.alert;
        window.alert = (msg) => {
            try {
                const els = this.ensureCompletionModal();
                const { overlay, modal, title, content, badges, closeBtn, continueBtn } = els;
                title.textContent = 'Notice';
                content.innerHTML = String(msg).replace(/\n/g, '<br>');
                badges.innerHTML = '';
                overlay.style.display = 'block';
                modal.style.display = 'block';
                const closeModal = () => {
                    modal.style.display = 'none';
                    overlay.style.display = 'none';
                    document.removeEventListener('keydown', escListener);
                };
                const escListener = (e) => { if (e.key === 'Escape') closeModal(); };
                closeBtn.onclick = closeModal;
                if (continueBtn) continueBtn.onclick = closeModal;
                overlay.onclick = closeModal;
                document.addEventListener('keydown', escListener);
            } catch (e) {
                originalAlert(msg);
            }
        };

        // Ensure modal/overlay are hidden on load
        const overlay = document.getElementById('modal-overlay');
        const modal = document.getElementById('completion-modal');
        if (overlay) overlay.style.display = 'none';
        if (modal) modal.style.display = 'none';

        this.bindEvents();
        this.updateDisplay();
        this.updateButtons();
    },

    bindEvents() {
        const startBtn = document.getElementById('start-btn');
        const pauseBtn = document.getElementById('pause-btn');
        const stopBtn = document.getElementById('stop-btn');
        const resetBtn = document.getElementById('reset-btn');
        const durationSelect = document.getElementById('duration-select');
        const subjectSelect = document.getElementById('subject-select');

        if (startBtn) {
            startBtn.onclick = () => this.start();
        }
        if (pauseBtn) {
            pauseBtn.onclick = () => this.pause();
        }
        if (stopBtn) {
            stopBtn.onclick = () => this.stop();
        }
        if (resetBtn) {
            resetBtn.onclick = () => this.reset();
        }
        if (durationSelect) {
            durationSelect.onchange = (e) => this.changeDuration(e.target.value);
        }
        if (subjectSelect) {
            subjectSelect.onchange = (e) => this.changeSubject(e.target.value);
        }
    },

    start() {
        
        if (this.isPaused) {
            // Resume
            this.isPaused = false;
            this.startTicking();
            this.updateStatus('Session resumed! Stay focused! 🚀');
        } else {
            // New session
            this.timeRemaining = this.selectedDuration * 60;
            this.isRunning = true;
            this.isPaused = false;
            this.startTicking();
            this.updateStatus('Session in progress... Stay focused! 🎯');
            this.createSession();
        }
        
        this.updateButtons();
        this.updateDisplay();
    },

    pause() {
        this.isPaused = true;
        this.stopTicking();
        this.updateStatus('Session paused. Click Start to resume. ⏸️');
        this.updateButtons();
    },

    stop() {
        const timeStudied = (this.selectedDuration * 60) - this.timeRemaining;
        const minutes = Math.floor(timeStudied / 60);
        
        if (minutes >= 1) {
            this.completeSession(minutes);
        } else {
            this.cancelSession();
        }
        
        this.reset();
    },

    reset() {
        this.isRunning = false;
        this.isPaused = false;
        this.stopTicking();
        this.timeRemaining = this.selectedDuration * 60;
        this.sessionId = null;
        this.updateDisplay();
        this.updateButtons();
        this.updateStatus('Ready to start your study session! 📚');
    },

    changeDuration(newDuration) {
        this.selectedDuration = parseInt(newDuration);
        if (!this.isRunning) {
            this.timeRemaining = this.selectedDuration * 60;
            this.updateDisplay();
        }
    },

    changeSubject(newSubject) {
        this.selectedSubject = newSubject;
    },

    startTicking() {
        this.stopTicking(); // Clear any existing interval
        this.intervalId = setInterval(() => {
            if (this.timeRemaining > 0) {
                this.timeRemaining--;
                this.updateDisplay();
            } else {
                // Prevent multiple completions by stopping the timer first
                this.stopTicking();
                this.isRunning = false;
                this.isPaused = false;
                this.updateButtons();
                this.completeSession(this.selectedDuration);
            }
        }, 1000);
    },

    stopTicking() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    },

    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const timeDisplay = document.getElementById('time-display');
        if (timeDisplay) {
            timeDisplay.textContent = timeString;
        }

        // Update page title when running
        if (this.isRunning && !this.isPaused) {
            document.title = `${timeString} - Study Timer`;
        } else {
            document.title = 'Study Streak Motivator';
        }

        // Update progress (simplified)
        const progressFill = document.getElementById('progress-fill');
        if (progressFill) {
            const totalTime = this.selectedDuration * 60;
            const progress = ((totalTime - this.timeRemaining) / totalTime) * 100;
            // Simple color change for progress indication
            progressFill.style.background = `linear-gradient(to top, #4285f4 ${progress}%, white ${progress}%)`;
        }
    },

    updateButtons() {
        const startBtn = document.getElementById('start-btn');
        const pauseBtn = document.getElementById('pause-btn');
        const stopBtn = document.getElementById('stop-btn');
        const resetBtn = document.getElementById('reset-btn');
        const durationSelect = document.getElementById('duration-select');
        const subjectSelect = document.getElementById('subject-select');

        if (!this.isRunning) {
            // Not started
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = '▶️ Start';
            }
            if (pauseBtn) pauseBtn.disabled = true;
            if (stopBtn) stopBtn.disabled = true;
            if (resetBtn) resetBtn.disabled = false;
            if (durationSelect) durationSelect.disabled = false;
            if (subjectSelect) subjectSelect.disabled = false;
        } else if (this.isPaused) {
            // Paused
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = '▶️ Resume';
            }
            if (pauseBtn) pauseBtn.disabled = true;
            if (stopBtn) stopBtn.disabled = false;
            if (resetBtn) resetBtn.disabled = false;
            if (durationSelect) durationSelect.disabled = true;
            if (subjectSelect) subjectSelect.disabled = true;
        } else {
            // Running
            if (startBtn) startBtn.disabled = true;
            if (pauseBtn) pauseBtn.disabled = false;
            if (stopBtn) stopBtn.disabled = false;
            if (resetBtn) resetBtn.disabled = true;
            if (durationSelect) durationSelect.disabled = true;
            if (subjectSelect) subjectSelect.disabled = true;
        }
    },

    updateStatus(message) {
        const statusText = document.getElementById('status-text');
        if (statusText) {
            statusText.textContent = message;
        }
    },

    async createSession() {
        try {
            const response = await fetch('/api/timer/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subject: this.selectedSubject,
                    duration: this.selectedDuration
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.sessionId = data.session_id;
            }
        } catch (error) {
            // Session creation failed, continue without server tracking
        }
    },

    async completeSession(minutes) {
        if (this.sessionId) {
            try {
                const response = await fetch('/api/timer/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: this.sessionId,
                        duration: minutes,
                        completed: true
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    this.showCompletionMessage(minutes, data.new_badges || []);
                } else {
                    this.showCompletionMessage(minutes, []);
                }
            } catch (error) {
                // Session completion failed, show local completion message
                this.showCompletionMessage(minutes, []);
            }
        } else {
            this.showCompletionMessage(minutes, []);
        }
    },

    async cancelSession() {
        if (this.sessionId) {
            try {
                await fetch(`/api/timer/cancel/${this.sessionId}`, {
                    method: 'DELETE'
                });
            } catch (error) {
                // Session cancellation failed, continue locally
            }
        }
        this.updateStatus('Session canceled. Ready to start again! 🔄');
    },

    ensureCompletionModal() {
        let overlay = document.getElementById('modal-overlay');
        let modal = document.getElementById('completion-modal');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'modal-overlay';
            overlay.className = 'modal-overlay';
            overlay.style.display = 'none';
            document.body.appendChild(overlay);
        }
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'completion-modal';
            modal.className = 'completion-modal';
            modal.style.display = 'none';
            modal.innerHTML = `
                <div class="modal-header">
                    <h2 id="modal-title">🎉 Session Complete!</h2>
                    <button id="modal-close-btn" class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <div id="modal-content"></div>
                    <div id="modal-badges"></div>
                </div>
                <div class="modal-footer">
                    <button id="modal-continue-btn" class="btn btn-primary">Continue</button>
                </div>
            `;
            document.body.appendChild(modal);
        }
        return {
            overlay,
            modal,
            title: document.getElementById('modal-title'),
            content: document.getElementById('modal-content'),
            badges: document.getElementById('modal-badges'),
            closeBtn: document.getElementById('modal-close-btn'),
            continueBtn: document.getElementById('modal-continue-btn')
        };
    },

    showCompletionMessage(minutes, newBadges) {
        const els = this.ensureCompletionModal();
        const { overlay, modal, title, content, badges, closeBtn, continueBtn } = els;

        title.textContent = '🎉 Session Complete!';
        content.innerHTML = `Great job! You studied <strong>${this.selectedSubject}</strong> for <strong>${minutes} minutes</strong>.`;

        // Badges list
        badges.innerHTML = '';
        if (newBadges && newBadges.length > 0) {
            const list = document.createElement('div');
            newBadges.forEach(b => {
                const item = document.createElement('div');
                item.className = 'new-badge';
                item.innerHTML = `<span class=\"badge-icon\">${b.icon || '🏆'}</span><span class=\"badge-name\">${b.name}</span>`;
                list.appendChild(item);
            });
            badges.appendChild(list);
            if (window.celebrateNewBadges) window.celebrateNewBadges(newBadges);
        }

        // Show modal
        overlay.style.display = 'block';
        modal.style.display = 'block';

        const closeModal = () => {
            modal.style.display = 'none';
            overlay.style.display = 'none';
            document.removeEventListener('keydown', escListener);
            this.reset();
        };

        const escListener = (e) => {
            if (e.key === 'Escape') closeModal();
        };

        closeBtn.onclick = closeModal;
        continueBtn.onclick = closeModal;
        overlay.onclick = closeModal;
        document.addEventListener('keydown', escListener);

        this.updateStatus('Session complete! Ready for another one? 🚀');
    },
    // Allow external close (used by modal "Continue" button)
    closeModal() {
        const overlay = document.getElementById('modal-overlay');
        const modal = document.getElementById('completion-modal');
        if (overlay) overlay.style.display = 'none';
        if (modal) modal.style.display = 'none';
        this.reset();
    }
};

// Expose timer globally for modal button handlers
window.timer = timer;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => timer.init());
} else {
    timer.init();
}