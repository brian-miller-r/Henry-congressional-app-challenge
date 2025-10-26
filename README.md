# 📚 Study Buddy

A gamified study tracking web app designed for 6th grade students participating in the Congressional App Challenge 2025.

## 🎯 Project Overview

Study Buddy helps students build consistent study habits through gamification. Students can track daily study sessions, maintain streaks, unlock achievement badges, and monitor their progress through an intuitive dashboard.

## ✨ Features (Planned)

- **Study Timer System** - Countdown timer with preset durations (5, 10, 15, 20, 30 minutes)
- **Streak Tracking** - Track consecutive days of study sessions
- **Achievement Badges** - Unlock badges for milestones (3-day streak, Week Warrior, Study Champion, etc.)
- **Progress Dashboard** - View study stats, subject breakdown, and calendar history
- **Subject Tracking** - Log study sessions by subject (Math, Science, English, History, Other)

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd ~/Projects/study-streak-motivator
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and visit:**
   ```
   http://127.0.0.1:5001
   ```

## 📁 Project Structure

```
study-streak-motivator/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Landing/welcome page
│   ├── dashboard.html     # Main dashboard (Phase 5)
│   └── timer.html         # Study timer page (Phase 3)
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   ├── js/                # JavaScript files (future phases)
│   └── img/
│       └── badges/        # Badge images (future phases)
└── instance/              # Database storage (auto-created)
```

## 🛠 Development Phases

###  Phase 1: Project Setup & Basic Structure (COMPLETE)
- [x] Virtual environment setup
- [x] Flask application initialization
- [x] Basic HTML templates and navigation
- [x] Responsive CSS styling
- [x] Project documentation

**Phase 2: Database Models & Setup**
- SQLAlchemy models (User, StudySession, Streak, Badge)
- Database initialization scripts

**Phase 3: Study Timer Implementation**
- Frontend timer component with countdown display
- JavaScript timer logic (start, pause, complete, reset)
- Subject selection and duration presets
- Session saving functionality

**Phase 4: Streak Calculation Logic**
- Algorithm to calculate current streak
- Database integration for streak tracking
- Handle edge cases (first session, missed days)

**Phase 5: Dashboard & Progress Tracking**
- Fetch and display user study data
- Current streak display with 🔥 emoji
- Study time statistics (today, week, all time)
- Calendar view of study history

**Phase 6: Badge/Achievement System**
- Badge unlocking logic and criteria
- Badge display on dashboard
- "New Badge Unlocked!" notifications

**Phase 7: UI Polish & Responsive Design**
- Enhanced animations and transitions
- Mobile optimization
- Celebration effects for milestones

**Phase 8: Testing & Bug Fixes**
- Comprehensive functionality testing
- Browser compatibility testing
- Edge case handling

## 🎨 Design System

### Color Scheme
- **Primary Blue:** #4285f4 (Google Blue)
- **Primary Green:** #34a853 (Success/Progress)
- **Primary Orange:** #fbbc05 (Call-to-action)
- **Primary Red:** #ea4335 (Alerts/Warnings)

### Typography
- **Primary Font:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Monospace Font:** Courier New (for timer display)

## 🧪 Testing

After setting up the project, test the following:

1. **Navigation:** All links work properly
2. **Responsive Design:** Test on mobile and desktop
3. **Page Loading:** All pages load without errors
4. **Visual Design:** Check layout and styling

## 🤝 Contributing

This project is built for educational purposes as part of the Congressional App Challenge. Future phases will add the core functionality step by step.

## 📝 License

This project is created for educational purposes for the Congressional App Challenge 2025.

## 🎯 Learning Objectives

Through building this project, students will learn:
- Flask web framework basics
- HTML/CSS responsive design
- JavaScript for interactive features
- Database concepts with SQLAlchemy
- Date/time handling in Python
- Algorithm design (streak calculation)
- Testing and debugging techniques
