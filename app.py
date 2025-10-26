"""
Study Streak Motivator - Main Flask Application
A gamified study tracking web app for students
Congressional App Challenge 2025
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from datetime import datetime, timedelta
import os
from models import db, User, StudySession, Streak, Badge, UserBadge, create_default_badges

# Create Flask application instance
app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("instance/study_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Disable static caching in debug to ensure newest JS/CSS are loaded
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize the database with the app
db.init_app(app)

# Create instance folder if it doesn't exist
os.makedirs('instance', exist_ok=True)

# Asset version for cache-busting static files in development
try:
    import time as _time
    ASSET_VERSION = str(int(_time.time()))
except Exception:
    ASSET_VERSION = "1"

@app.context_processor
def inject_asset_version():
    return {'asset_version': ASSET_VERSION}



# Performance optimizations
@app.after_request
def after_request(response):
    """Add performance headers to all responses"""
    # Cache static files (disabled in debug)
    if request.path.startswith('/static/'):
        if app.debug:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        else:
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            response.headers['Expires'] = (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        # Disable caching for HTML responses during development to prevent stale pages
        if 'text/html' in response.headers.get('Content-Type', ''):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Performance headers
    response.headers['Vary'] = 'Accept-Encoding'
    
    return response

@app.route('/')
def index():
    """
    Home page route - Welcome page for new users
    Shows project introduction and motivation to start studying
    """
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """
    Dashboard route - Main user interface showing real database data
    Shows study streaks, badges, and progress from Phase 2
    """
    from db_utils import get_dashboard_data
    
    # Get the default user for now (in Phase 4+ we'll add proper user sessions)
    user_id = 1  # Default 'student' user
    dashboard_data = get_dashboard_data(user_id)
    
    if not dashboard_data:
        flash('User not found. Please initialize the database.', 'error')
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/dashboard/enhanced')
def dashboard_enhanced():
    """
    Enhanced Dashboard route - Phase 5 advanced analytics dashboard
    Shows interactive charts, detailed analytics, and smart insights
    """
    from db_utils import get_dashboard_data
    
    # Get the default user for now (in Phase 4+ we'll add proper user sessions)
    user_id = 1  # Default 'student' user
    dashboard_data = get_dashboard_data(user_id)
    
    if not dashboard_data:
        flash('User not found. Please initialize the database.', 'error')
        return redirect(url_for('index'))
    
    return render_template('dashboard_enhanced.html', data=dashboard_data)

@app.route('/timer')
def timer():
    """
    Study Timer route - Where students will track study sessions
    Will include countdown timer and subject selection (Phase 3)
    """
    # Placeholder for timer functionality
    return render_template('timer.html')

@app.route('/history')
def study_history():
    """
    Study History route - Detailed view of all study sessions
    Phase 5 feature with filtering and search capabilities
    """
    from db_utils import get_study_history_data
    
    # Get the default user for now
    user_id = 1  # Default 'student' user
    history_data = get_study_history_data(user_id)
    
    if not history_data:
        flash('User not found. Please initialize the database.', 'error')
        return redirect(url_for('index'))
    
    return render_template('history.html', data=history_data)

@app.route('/badges')
def badges():
    """Badge Collection page - Phase 6/7 enhancement."""
    try:
        # Get all badges
        all_badges = Badge.query.order_by(Badge.category, Badge.tier, Badge.name).all()
        
        # Get earned badges for user 1 (test user)
        earned_user_badges = UserBadge.query.filter_by(user_id=1).all()
        earned_badge_ids = {ub.badge_id for ub in earned_user_badges}
        earned_badges_dict = {ub.badge_id: ub for ub in earned_user_badges}
        
        # Calculate badge statistics
        total_points = sum(badge.points for badge in all_badges if badge.id in earned_badge_ids)
        completion_percentage = round((len(earned_badge_ids) / len(all_badges)) * 100) if all_badges else 0
        rare_badges_count = len([b for b in all_badges if b.rarity in ['epic', 'legendary'] and b.id in earned_badge_ids])
        
        return render_template('badges.html',
                             badges=all_badges,
                             earned_badges=earned_user_badges,
                             earned_badge_ids=earned_badge_ids,
                             earned_badges_dict=earned_badges_dict,
                             total_points=total_points,
                             completion_percentage=completion_percentage,
                             rare_badges_count=rare_badges_count)
    except Exception as e:
        print(f"Badge collection error: {e}")
        # Fallback for when database isn't initialized
        return render_template('badges.html',
                             badges=[],
                             earned_badges=[],
                             earned_badge_ids=set(),
                             earned_badges_dict={},
                             total_points=0,
                             completion_percentage=0,
                             rare_badges_count=0)

@app.route('/init-db')
def init_database():
    """
    Initialize the database with tables and default data
    For development use - should be called once to set up the database
    """
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Create default badges
            create_default_badges()
            
            # Create a default user for testing (optional)
            default_user = User.query.filter_by(username='student').first()
            if not default_user:
                default_user = User(username='student', email='student@example.com')
                db.session.add(default_user)
                db.session.commit()
            
        flash('Database initialized successfully!', 'success')
        return jsonify({
            'status': 'success',
            'message': 'Database and default data created successfully!',
            'tables': ['users', 'study_sessions', 'streaks', 'badges', 'user_badges']
        })
    except Exception as e:
        flash(f'Database initialization failed: {str(e)}', 'error')
        return jsonify({
            'status': 'error',
            'message': f'Database initialization failed: {str(e)}'
        }), 500

@app.route('/db-status')
def database_status():
    """
    Check database status and show table information
    Useful for development and debugging
    """
    try:
        with app.app_context():
            # Count records in each table
            user_count = User.query.count()
            session_count = StudySession.query.count()
            streak_count = Streak.query.count()
            badge_count = Badge.query.count()
            user_badge_count = UserBadge.query.count()
            
        return jsonify({
            'status': 'connected',
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
            'table_counts': {
                'users': user_count,
                'study_sessions': session_count,
                'streaks': streak_count,
                'badges': badge_count,
                'user_badges': user_badge_count
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }), 500

# Timer API Endpoints
@app.route('/api/timer/start', methods=['POST'])
def start_timer_session():
    """
    Start a new study session
    """
    from db_utils import create_study_session
    
    try:
        data = request.get_json()
        subject = data.get('subject', 'Math')
        duration = data.get('duration', 25)
        
        # For now, use default user (ID: 1)
        # In future phases, we'll use proper user authentication
        user_id = 1
        
        # Create study session
        session = create_study_session(user_id, subject, duration)
        
        return jsonify({
            'status': 'success',
            'session_id': session.id,
            'subject': session.subject,
            'duration': session.duration_minutes
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to start session: {str(e)}'
        }), 500

@app.route('/api/timer/complete', methods=['POST'])
def complete_timer_session():
    """
    Complete a study session and update progress
    """
    from db_utils import complete_study_session, check_and_award_badges, update_streak
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        duration = data.get('duration')
        completed = data.get('completed', True)
        
        if not session_id:
            return jsonify({
                'status': 'error',
                'message': 'Session ID is required'
            }), 400
            
        # Get the session and update it
        session = db.session.get(StudySession, session_id)
        if not session:
            return jsonify({
                'status': 'error',
                'message': 'Session not found'
            }), 404
            
        # Update session details
        session.duration_minutes = duration
        session.completed = completed
        db.session.commit()
        
        # Update streak if session was completed
        streak_update_info = {}
        if completed:
            from streak_calculator import get_streak_status
            streak_update_info = update_streak(session.user_id)
            # Get full streak status for response
            streak_status = get_streak_status(session.user_id)
            
        # Check for new badges
        new_badges = check_and_award_badges(session.user_id)
        
        response_data = {
            'status': 'success',
            'session_id': session.id,
            'duration': session.duration_minutes,
            'completed': session.completed,
            'new_badges': [
                {
                    'id': badge.id,
                    'name': badge.name,
                    'icon': badge.icon,
                    'description': badge.description
                } for badge in new_badges
            ]
        }
        
        # Add streak information if session was completed
        if completed and 'streak_status' in locals():
            response_data['streak'] = {
                'current_streak': streak_status['current_streak'],
                'longest_streak': streak_status['longest_streak'],
                'message': streak_status['message'],
                'new_record': streak_status['is_new_record']
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to complete session: {str(e)}'
        }), 500

@app.route('/api/calendar-data')
def get_calendar_data():
    """
    Get calendar data for study activity visualization
    """
    from streak_calculator import get_streak_calendar_data
    
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        user_id = 1  # Default user for now
        
        calendar_data = get_streak_calendar_data(user_id, year, month)
        
        return jsonify({
            'status': 'success',
            'calendar_data': calendar_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get calendar data: {str(e)}'
        }), 500

@app.route('/api/streak/<int:user_id>')
def get_streak_info(user_id):
    """
    Get comprehensive streak information for a user
    """
    from streak_calculator import get_streak_status, get_streak_calendar_data
    
    try:
        streak_status = get_streak_status(user_id)
        calendar_data = get_streak_calendar_data(user_id)
        
        return jsonify({
            'status': 'success',
            'streak_info': streak_status,
            'calendar_data': calendar_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get streak info: {str(e)}'
        }), 500

@app.route('/api/timer/cancel/<int:session_id>', methods=['DELETE'])
def cancel_timer_session(session_id):
    """
    Cancel a study session (delete it from database)
    """
    try:
        session = db.session.get(StudySession, session_id)
        if session:
            db.session.delete(session)
            db.session.commit()
            
        return jsonify({
            'status': 'success',
            'message': 'Session canceled'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to cancel session: {str(e)}'
        }), 500

# Error handlers for better user experience
@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors with a friendly message"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors gracefully"""
    return render_template('index.html'), 500

# Run the application in development mode
if __name__ == '__main__':
    # Debug mode enabled for development
    # In production, set debug=False
    app.run(debug=True, host='127.0.0.1', port=3333)
