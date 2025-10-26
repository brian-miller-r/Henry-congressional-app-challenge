/**
 * Study Calendar Component
 * Interactive calendar showing study activity and streaks
 * Phase 5 Enhancement - Congressional App Challenge 2025
 */

class StudyCalendar {
    constructor(containerId, data = {}) {
        this.container = document.getElementById(containerId);
        this.data = data;
        this.currentMonth = new Date().getMonth();
        this.currentYear = new Date().getFullYear();
        this.months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        this.weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            return;
        }
        
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="calendar-header">
                <button class="calendar-nav-btn" id="prevMonth">‹</button>
                <h3 class="calendar-title">
                    ${this.months[this.currentMonth]} ${this.currentYear}
                </h3>
                <button class="calendar-nav-btn" id="nextMonth">›</button>
            </div>
            <div class="calendar-weekdays">
                ${this.weekdays.map(day => `<div class="weekday">${day}</div>`).join('')}
            </div>
            <div class="calendar-grid">
                ${this.generateCalendarDays()}
            </div>
            <div class="calendar-legend">
                <div class="legend-item">
                    <div class="legend-color no-activity"></div>
                    <span>No Study</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color light-activity"></div>
                    <span>Light (< 30 min)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color medium-activity"></div>
                    <span>Medium (30-60 min)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color high-activity"></div>
                    <span>High (> 60 min)</span>
                </div>
            </div>
        `;
    }
    
    generateCalendarDays() {
        const firstDay = new Date(this.currentYear, this.currentMonth, 1);
        const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
        const firstDayOfWeek = firstDay.getDay();
        const daysInMonth = lastDay.getDate();
        
        let daysHTML = '';
        
        // Add empty cells for days before the first day of the month
        for (let i = 0; i < firstDayOfWeek; i++) {
            daysHTML += '<div class="calendar-day empty"></div>';
        }
        
        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const studyData = this.data[dateStr] || { total_study_minutes: 0, has_streak_activity: false };
            const isToday = this.isToday(day);
            
            const activityClass = this.getActivityClass(studyData.total_study_minutes);
            const todayClass = isToday ? ' today' : '';
            const streakClass = studyData.has_streak_activity ? ' streak-day' : '';
            
            daysHTML += `
                <div class="calendar-day${todayClass}${streakClass} ${activityClass}" 
                     data-date="${dateStr}" 
                     data-minutes="${studyData.total_study_minutes}"
                     title="${this.getDayTooltip(day, studyData)}">
                    <span class="day-number">${day}</span>
                    ${studyData.total_study_minutes > 0 ? `<span class="study-time">${studyData.total_study_minutes}m</span>` : ''}
                </div>
            `;
        }
        
        return daysHTML;
    }
    
    getActivityClass(minutes) {
        if (minutes === 0) return 'no-activity';
        if (minutes < 30) return 'light-activity';
        if (minutes < 60) return 'medium-activity';
        return 'high-activity';
    }
    
    isToday(day) {
        const today = new Date();
        return today.getDate() === day && 
               today.getMonth() === this.currentMonth && 
               today.getFullYear() === this.currentYear;
    }
    
    getDayTooltip(day, studyData) {
        const date = new Date(this.currentYear, this.currentMonth, day);
        const dateStr = date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        if (studyData.total_study_minutes > 0) {
            return `${dateStr}: ${studyData.total_study_minutes} minutes studied`;
        } else {
            return `${dateStr}: No study activity`;
        }
    }
    
    attachEventListeners() {
        const prevBtn = document.getElementById('prevMonth');
        const nextBtn = document.getElementById('nextMonth');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                this.currentMonth--;
                if (this.currentMonth < 0) {
                    this.currentMonth = 11;
                    this.currentYear--;
                }
                this.fetchDataAndRender();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.currentMonth++;
                if (this.currentMonth > 11) {
                    this.currentMonth = 0;
                    this.currentYear++;
                }
                this.fetchDataAndRender();
            });
        }
        
        // Add click handlers for calendar days
        this.container.addEventListener('click', (e) => {
            const dayElement = e.target.closest('.calendar-day');
            if (dayElement && !dayElement.classList.contains('empty')) {
                this.handleDayClick(dayElement);
            }
        });
    }
    
    handleDayClick(dayElement) {
        const date = dayElement.dataset.date;
        const minutes = dayElement.dataset.minutes;
        
        // Remove previous selection
        this.container.querySelectorAll('.calendar-day.selected').forEach(day => {
            day.classList.remove('selected');
        });
        
        // Add selection to clicked day
        dayElement.classList.add('selected');
        
        // Emit custom event for day selection
        const event = new CustomEvent('daySelected', {
            detail: { date, minutes: parseInt(minutes) }
        });
        this.container.dispatchEvent(event);
    }
    
    async fetchDataAndRender() {
        try {
            // Fetch new data for the current month
            const response = await fetch(`/api/calendar-data?year=${this.currentYear}&month=${this.currentMonth + 1}`);
            if (response.ok) {
                const newData = await response.json();
                this.data = newData.calendar_data || {};
            }
        } catch (error) {
            // Failed to fetch calendar data, use existing data
        }
        
        this.render();
        this.attachEventListeners();
    }
    
    updateData(newData) {
        this.data = newData;
        this.render();
        this.attachEventListeners();
    }
}

// Export for use in other scripts
window.StudyCalendar = StudyCalendar;