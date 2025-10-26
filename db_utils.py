"""
Database utility functions for Study Streak Motivator
Common CRUD operations and helper functions
"""

from datetime import date, datetime, timedelta
from models import db, User, StudySession, Streak, Badge, UserBadge
from sqlalchemy import func

# User Functions
def create_user(username, email=None):
    """Create a new user"""
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)

# Study Session Functions
def create_study_session(user_id, subject, duration_minutes, session_date=None):
    """Create a new study session"""
    if session_date is None:
        session_date = date.today()
    
    session = StudySession(
        user_id=user_id,
        subject=subject,
        duration_minutes=duration_minutes,
        session_date=session_date,
        start_time=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()
    return session

def get_user_sessions(user_id, limit=None):
    """Get all study sessions for a user"""
    query = StudySession.query.filter_by(user_id=user_id).order_by(StudySession.start_time.desc())
    if limit:
        query = query.limit(limit)
    return query.all()

def get_sessions_by_date(user_id, session_date):
    """Get study sessions for a specific date"""
    return StudySession.query.filter_by(
        user_id=user_id, 
        session_date=session_date
    ).all()

def get_total_study_time(user_id, days=None):
    """Get total study time for a user (optionally within last N days)"""
    query = StudySession.query.filter_by(user_id=user_id, completed=True)
    
    if days:
        since_date = date.today() - timedelta(days=days)
        query = query.filter(StudySession.session_date >= since_date)
    
    sessions = query.all()
    return sum(session.duration_minutes for session in sessions)

def get_study_stats_by_subject(user_id, days=30):
    """Get study time breakdown by subject"""
    since_date = date.today() - timedelta(days=days)
    
    results = db.session.query(
        StudySession.subject,
        func.sum(StudySession.duration_minutes).label('total_minutes'),
        func.count(StudySession.id).label('session_count')
    ).filter(
        StudySession.user_id == user_id,
        StudySession.completed == True,
        StudySession.session_date >= since_date
    ).group_by(StudySession.subject).all()
    
    return [
        {
            'subject': result.subject,
            'total_minutes': result.total_minutes or 0,
            'session_count': result.session_count
        }
        for result in results
    ]

# Streak Functions
def get_current_streak(user_id):
    """Get the user's current active streak"""
    return Streak.query.filter_by(user_id=user_id, is_active=True).first()

def update_streak(user_id):
    """Update user's streak based on study activity - Enhanced Phase 4 version"""
    from streak_calculator import streak_calculator
    return streak_calculator.update_user_streak(user_id)

# Badge Functions
def check_and_award_badges(user_id):
    """Check if user has earned any new badges - Enhanced Phase 6 version"""
    try:
        from badge_engine import check_and_award_badges as engine_check_badges
        return engine_check_badges(user_id)
    except ImportError:
        # Fallback to basic checking if badge engine not available
        user = get_user_by_id(user_id)
        if not user:
            return []
        
        # Get all badges user hasn't earned yet
        earned_badge_ids = [ub.badge_id for ub in user.user_badges]
        available_badges = Badge.query.filter(~Badge.id.in_(earned_badge_ids)).all()
        
        newly_earned = []
        
        for badge in available_badges:
            earned = False
            
            if badge.criteria_type == 'sessions':
                session_count = StudySession.query.filter_by(user_id=user_id, completed=True).count()
                earned = session_count >= badge.criteria_value
            
            elif badge.criteria_type == 'streak':
                current_streak = get_current_streak(user_id)
                if current_streak:
                    earned = current_streak.current_days >= badge.criteria_value
            
            elif badge.criteria_type == 'time':
                total_minutes = get_total_study_time(user_id)
                earned = total_minutes >= badge.criteria_value
            
            if earned:
                # Award the badge
                user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                db.session.add(user_badge)
                newly_earned.append(badge)
        
        db.session.commit()
        return newly_earned

def get_user_badges(user_id):
    """Get all badges earned by a user"""
    return db.session.query(Badge).join(UserBadge).filter(
        UserBadge.user_id == user_id
    ).order_by(UserBadge.earned_at.desc()).all()

def get_available_badges(user_id):
    """Get badges the user hasn't earned yet"""
    earned_badge_ids = [ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).all()]
    return Badge.query.filter(~Badge.id.in_(earned_badge_ids)).all()

# Enhanced Dashboard Analytics Functions
def get_study_time_trends(user_id, days=30):
    """Get daily study time trends for the last N days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    # Get sessions grouped by date
    results = db.session.query(
        StudySession.session_date,
        func.sum(StudySession.duration_minutes).label('total_minutes')
    ).filter(
        StudySession.user_id == user_id,
        StudySession.completed == True,
        StudySession.session_date >= start_date,
        StudySession.session_date <= end_date
    ).group_by(StudySession.session_date).all()
    
    # Create data for all days (including zeros)
    trends = {}
    current_date = start_date
    while current_date <= end_date:
        trends[current_date.isoformat()] = 0
        current_date += timedelta(days=1)
    
    # Fill in actual data
    for result in results:
        trends[result.session_date.isoformat()] = result.total_minutes or 0
    
    return trends

def get_weekly_comparison(user_id):
    """Compare this week vs last week study performance"""
    today = date.today()
    
    # This week (last 7 days)
    this_week_start = today - timedelta(days=6)
    this_week_total = get_total_study_time(user_id, days=7)
    
    # Last week (days 7-13 ago)
    last_week_start = today - timedelta(days=13)
    last_week_end = today - timedelta(days=7)
    
    last_week_sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.completed == True,
        StudySession.session_date >= last_week_start,
        StudySession.session_date <= last_week_end
    ).all()
    
    last_week_total = sum(session.duration_minutes for session in last_week_sessions)
    
    # Calculate change
    if last_week_total > 0:
        change_percent = ((this_week_total - last_week_total) / last_week_total) * 100
    else:
        change_percent = 100 if this_week_total > 0 else 0
    
    return {
        'this_week': this_week_total,
        'last_week': last_week_total,
        'change_percent': round(change_percent, 1),
        'trend': 'up' if change_percent > 0 else 'down' if change_percent < 0 else 'same'
    }

def get_study_hour_analysis(user_id, days=30):
    """Analyze what hours of day user studies most"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.completed == True,
        StudySession.session_date >= start_date
    ).all()
    
    hour_data = {}
    for hour in range(24):
        hour_data[hour] = 0
    
    for session in sessions:
        if session.start_time:
            hour = session.start_time.hour
            hour_data[hour] += session.duration_minutes
    
    # Find peak hours
    peak_hour = max(hour_data, key=hour_data.get) if sessions else 12
    peak_minutes = hour_data[peak_hour]
    
    return {
        'hourly_data': hour_data,
        'peak_hour': peak_hour,
        'peak_minutes': peak_minutes,
        'peak_time_display': f"{peak_hour}:00" if peak_hour < 12 else f"{peak_hour}:00" if peak_hour == 12 else f"{peak_hour-12}:00"
    }

def get_streak_history(user_id, limit=10):
    """Get historical streak data for visualization"""
    streaks = Streak.query.filter_by(user_id=user_id).order_by(Streak.created_at.desc()).limit(limit).all()
    
    streak_data = []
    for streak in streaks:
        streak_data.append({
            'days': streak.current_days,
            'start_date': streak.start_date.isoformat(),
            'end_date': streak.end_date.isoformat() if streak.end_date else None,
            'is_active': streak.is_active,
            'created_at': streak.created_at.isoformat()
        })
    
    return streak_data

def get_goal_progress(user_id):
    """Get progress toward study goals (placeholder for future goal system)"""
    today = date.today()
    
    # Default daily goal (can be customized later)
    daily_goal_minutes = 60  # 1 hour default
    weekly_goal_minutes = 300  # 5 hours default
    
    # Today's progress
    today_minutes = get_total_study_time(user_id, days=1)
    daily_progress = min(100, (today_minutes / daily_goal_minutes) * 100)
    
    # This week's progress
    weekly_minutes = get_total_study_time(user_id, days=7)
    weekly_progress = min(100, (weekly_minutes / weekly_goal_minutes) * 100)
    
    return {
        'daily': {
            'current': today_minutes,
            'goal': daily_goal_minutes,
            'progress_percent': round(daily_progress, 1),
            'completed': daily_progress >= 100
        },
        'weekly': {
            'current': weekly_minutes,
            'goal': weekly_goal_minutes,
            'progress_percent': round(weekly_progress, 1),
            'completed': weekly_progress >= 100
        }
    }

# Dashboard Data Functions
def get_dashboard_data(user_id):
    """Get all data needed for the user dashboard - Enhanced Phase 4 version"""
    user = get_user_by_id(user_id)
    if not user:
        return None
    
    from streak_calculator import get_streak_status
    
    current_streak = get_current_streak(user_id)
    recent_sessions = get_user_sessions(user_id, limit=10)
    earned_badges = get_user_badges(user_id)
    subject_stats = get_study_stats_by_subject(user_id)
    
    # Get enhanced streak information
    streak_status = get_streak_status(user_id)
    
    # Get enhanced analytics data
    study_trends = get_study_time_trends(user_id, days=14)  # Last 2 weeks
    weekly_comparison = get_weekly_comparison(user_id)
    hour_analysis = get_study_hour_analysis(user_id)
    streak_history = get_streak_history(user_id, limit=5)
    goal_progress = get_goal_progress(user_id)
    
    return {
        'user': user,
        'current_streak': streak_status['current_streak'],
        'longest_streak': streak_status['longest_streak'],
        'streak_status': streak_status['status'],
        'streak_message': streak_status['message'],
        'has_studied_today': streak_status['has_studied_today'],
        'today_study_minutes': streak_status['today_study_minutes'],
        'total_study_time': get_total_study_time(user_id),
        'weekly_study_time': get_total_study_time(user_id, days=7),
        'total_sessions': StudySession.query.filter_by(user_id=user_id, completed=True).count(),
        'recent_sessions': recent_sessions,
        'earned_badges': earned_badges,
        'subject_stats': subject_stats,
        # Enhanced Phase 5 analytics
        'study_trends': study_trends,
        'weekly_comparison': weekly_comparison,
        'hour_analysis': hour_analysis,
        'streak_history': streak_history,
        'goal_progress': goal_progress
    }

# Utility Functions
def complete_study_session(session_id):
    """Mark a study session as completed and check for badge awards"""
    session = StudySession.query.get(session_id)
    if session:
        session.mark_completed()
        
        # Update streak
        update_streak(session.user_id)
        
        # Check for new badges
        new_badges = check_and_award_badges(session.user_id)
        
        return session, new_badges
    return None, []

def get_study_calendar_data(user_id, year=None, month=None):
    """Get study session data for calendar view"""
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month
    
    # Get first and last day of the month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.session_date >= first_day,
        StudySession.session_date <= last_day,
        StudySession.completed == True
    ).all()
    
    # Group by date
    calendar_data = {}
    for session in sessions:
        date_str = session.session_date.isoformat()
        if date_str not in calendar_data:
            calendar_data[date_str] = {
                'sessions': 0,
                'total_minutes': 0,
                'subjects': set()
            }
        calendar_data[date_str]['sessions'] += 1
        calendar_data[date_str]['total_minutes'] += session.duration_minutes
        calendar_data[date_str]['subjects'].add(session.subject)
    
    # Convert sets to lists for JSON serialization
    for date_str in calendar_data:
        calendar_data[date_str]['subjects'] = list(calendar_data[date_str]['subjects'])
    
    return calendar_data


def get_study_history_data(user_id):
    """Get comprehensive study history data for the history page"""
    user = get_user_by_id(user_id)
    if not user:
        return None
    
    # Get all sessions ordered by date (newest first)
    sessions = StudySession.query.filter_by(user_id=user_id).order_by(StudySession.session_date.desc(), StudySession.start_time.desc()).all()
    
    if not sessions:
        return {
            'user': user,
            'sessions': [],
            'subjects': [],
            'total_time': 0,
            'completed_count': 0
        }
    
    # Get unique subjects
    subjects = list(set(session.subject for session in sessions))
    subjects.sort()
    
    # Calculate totals
    total_time = sum(session.duration_minutes for session in sessions if session.duration_minutes)
    completed_count = sum(1 for session in sessions if session.completed)
    
    return {
        'user': user,
        'sessions': sessions,
        'subjects': subjects,
        'total_time': total_time,
        'completed_count': completed_count
    }
