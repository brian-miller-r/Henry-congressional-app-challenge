# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Study Streak Motivator is a gamified study tracking web application built for 6th grade students participating in the Congressional App Challenge 2025. The app helps students build consistent study habits through gamification, tracking daily study sessions, maintaining streaks, and unlocking achievement badges.

## Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLAlchemy 3.1.1 with SQLite (planned for Phase 2)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Styling**: Custom CSS with responsive design and CSS Grid/Flexbox
- **Date Handling**: python-dateutil 2.8.2 (for streak calculations)

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start development server
python app.py
# Server runs on http://127.0.0.1:5001

# Alternative run methods
python -m flask run --port=5001
flask --app app.py run --debug --port=5001
```

### Database Operations (Future Phases)
```bash
# Initialize database (when SQLAlchemy is integrated)
python -c "from app import db; db.create_all()"
```

## Architecture Overview

### Application Structure
The application follows a standard Flask MVC pattern with a phased development approach:

```
study-streak-motivator/
├── app.py                  # Main Flask application with routes
├── requirements.txt        # Python dependencies
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation and layout
│   ├── index.html         # Landing/welcome page
│   ├── dashboard.html     # Main dashboard (Phase 5)
│   └── timer.html         # Study timer page (Phase 3)
├── static/
│   ├── css/style.css      # Main stylesheet with design system
│   ├── js/               # JavaScript files (future phases)
│   └── img/badges/       # Badge images (Phase 6)
└── instance/             # SQLite database storage (auto-created)
```

### Key Components

1. **Flask Application (app.py)**
   - Single-file Flask app with route definitions
   - Error handlers for 404/500 errors
   - Configuration for SQLAlchemy database (planned)
   - Runs on localhost:5001 in debug mode

2. **Template System**
   - `base.html`: Shared layout with navigation, flash messages, responsive mobile menu
   - Route-specific templates extend base template
   - Uses Jinja2 templating with Flask's `url_for()` for URLs

3. **CSS Design System**
   - Google-inspired color palette (primary blue, green, orange, red)
   - Mobile-first responsive design with breakpoints at 768px and 480px
   - CSS Grid and Flexbox for layouts
   - Custom animations and transitions
   - Component-based styling (cards, buttons, navigation)

### Development Phases

The application is built in 9 planned phases:

- **Phase 1** ✅: Basic Flask setup and responsive UI
- **Phase 2** ✅: Database models (User, StudySession, Streak, Badge)
- **Phase 3**: Study timer with JavaScript countdown functionality
- **Phase 4**: Streak calculation algorithms
- **Phase 5**: Dashboard with progress tracking and statistics
- **Phase 6**: Badge/achievement system
- **Phase 7**: UI polish and animations
- **Phase 8**: Testing and bug fixes
- **Phase 9**: Advanced Gamification
  - Customizable avatars with unlockable features
  - Virtual currency system for rewards
  - Character progression and skill trees
  - Achievement-based item shop
  - Interactive rewards (like Blooket/Gimkit)
  - Daily challenges and quests
  - Social features (leaderboards, friend system)
  - Character customization interface

### Current State
Currently in Phase 1 - basic Flask application with responsive UI templates. All routes return static template content with placeholders for future functionality.

## Database Design (Phase 2 Planning)

When implementing SQLAlchemy models, the planned schema includes:
- `User`: Student profiles and settings
- `StudySession`: Individual timed study sessions with subject tracking
- `Streak`: Daily streak calculations and history
- `Badge`: Achievement system with unlock criteria

## Frontend Architecture

### CSS Organization
- **Variables**: Custom CSS properties for consistent theming
- **Layout**: Container-based responsive grid system
- **Components**: Modular styles for cards, buttons, navigation, forms
- **Mobile Navigation**: Hamburger menu with slide-out functionality
- **Animations**: Keyframe animations for page transitions and interactions

### JavaScript Integration (Future)
- Study timer functionality will use vanilla JavaScript
- Local storage for session persistence
- AJAX for database interactions without page reloads

## Key Files for Development

When working on this project, the most important files to understand are:

1. **`app.py`** - Central application logic and routing
2. **`templates/base.html`** - Shared layout and navigation structure
3. **`static/css/style.css`** - Complete design system and responsive styles
4. **`requirements.txt`** - Dependencies (minimal Flask stack)

## Design System Colors
- **Primary Blue**: #4285f4 (Google Blue)
- **Primary Green**: #34a853 (Success/Progress)
- **Primary Orange**: #fbbc05 (Call-to-action)
- **Primary Red**: #ea4335 (Alerts/Warnings)

## Development Workflow

1. The application uses Flask's debug mode for auto-reloading during development
2. Static files are served through Flask's built-in static file serving
3. Templates use Jinja2 inheritance for consistent layout
4. Future database work will use SQLAlchemy ORM with SQLite
5. No build process or bundling required - direct file serving

## Project Context

This is an educational project for middle school students learning web development concepts including Flask basics, HTML/CSS responsive design, JavaScript interactivity, database concepts, and algorithm design for streak calculations.