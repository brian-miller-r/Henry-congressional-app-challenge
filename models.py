"""
Database Models for Study Streak Motivator
Congressional App Challenge 2025
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    """
    User model for student profiles
    Simple model for Phase 2 - can be expanded later
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    study_sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")
    streaks = relationship("Streak", back_populates="user", cascade="all, delete-orphan")
    user_badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_current_streak(self):
        """Get the user's current active streak"""
        latest_streak = Streak.query.filter_by(
            user_id=self.id, 
            is_active=True
        ).first()
        return latest_streak.current_days if latest_streak else 0
    
    def get_total_study_time(self):
        """Get total study time in minutes"""
        sessions = StudySession.query.filter_by(user_id=self.id).all()
        return sum(session.duration_minutes for session in sessions if session.duration_minutes)

class StudySession(db.Model):
    """
    Study Session model to track individual study periods
    """
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)  # Math, Science, English, History, Other
    duration_minutes = db.Column(db.Integer, nullable=False)
    session_date = db.Column(db.Date, default=date.today)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    
    def __repr__(self):
        return f'<StudySession {self.subject} - {self.duration_minutes}min>'
    
    def mark_completed(self):
        """Mark session as completed and update completion time"""
        self.completed = True
        db.session.commit()

class Streak(db.Model):
    """
    Streak model to track consecutive study days
    """
    __tablename__ = 'streaks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # NULL if streak is active
    current_days = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="streaks")
    
    def __repr__(self):
        return f'<Streak {self.current_days} days - {"Active" if self.is_active else "Ended"}>'
    
    def extend_streak(self):
        """Extend the current streak by one day"""
        if self.is_active:
            self.current_days += 1
            db.session.commit()
    
    def break_streak(self):
        """End the current streak"""
        self.is_active = False
        self.end_date = date.today()
        db.session.commit()

class Badge(db.Model):
    """
    Enhanced Badge model for comprehensive achievement system - Phase 6
    """
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), nullable=False)  # Emoji or icon identifier
    
    # Enhanced Phase 6 fields
    category = db.Column(db.String(50), nullable=False, default='general')  # streak, time, consistency, subject, special
    tier = db.Column(db.String(20), nullable=False, default='bronze')  # bronze, silver, gold, platinum, legendary
    rarity = db.Column(db.String(20), nullable=False, default='common')  # common, rare, epic, legendary
    points = db.Column(db.Integer, nullable=False, default=10)  # Points awarded for earning this badge
    
    # Criteria fields (more flexible than before)
    criteria_type = db.Column(db.String(50), nullable=False)  # 'streak', 'sessions', 'time', 'consistency', 'subject', 'special'
    criteria_value = db.Column(db.Integer, nullable=False)  # Required value to unlock
    criteria_details = db.Column(db.Text, nullable=True)  # JSON string for complex criteria
    
    # Display and sharing
    color = db.Column(db.String(7), nullable=False, default='#4285f4')  # Hex color for badge
    is_secret = db.Column(db.Boolean, default=False)  # Hidden until earned
    is_active = db.Column(db.Boolean, default=True)  # Can be disabled
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Badge {self.name} ({self.tier} {self.rarity})>'
    
    def get_criteria_details(self):
        """Parse criteria_details JSON if present"""
        if self.criteria_details:
            try:
                import json
                return json.loads(self.criteria_details)
            except:
                return {}
        return {}
    
    def set_criteria_details(self, details_dict):
        """Set criteria_details as JSON string"""
        import json
        self.criteria_details = json.dumps(details_dict)

class UserBadge(db.Model):
    """
    Junction table for users and their earned badges
    """
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")
    
    # Ensure a user can only earn each badge once
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)
    
    def __repr__(self):
        return f'<UserBadge User:{self.user_id} Badge:{self.badge_id}>'

def create_default_badges():
    """
    Create comprehensive badges for the application - Phase 6 Enhanced
    Called during database initialization
    """
    try:
        from badge_definitions import create_advanced_badges
        return create_advanced_badges()
    except ImportError:
        # Fallback to basic badges if advanced system not available
        default_badges = [
            {
                'name': 'Getting Started',
                'description': 'Complete your first study session',
                'icon': '🌟',
                'criteria_type': 'sessions',
                'criteria_value': 1
            },
            {
                'name': 'Three Day Streak',
                'description': 'Study for 3 consecutive days',
                'icon': '🔥',
                'criteria_type': 'streak',
                'criteria_value': 3
            },
            {
                'name': 'Week Warrior',
                'description': 'Study for 7 consecutive days',
                'icon': '⚡',
                'criteria_type': 'streak',
                'criteria_value': 7
            },
            {
                'name': 'Study Champion',
                'description': 'Study for 30 consecutive days',
                'icon': '🏆',
                'criteria_type': 'streak',
                'criteria_value': 30
            },
            {
                'name': '10 Sessions',
                'description': 'Complete 10 study sessions',
                'icon': '📚',
                'criteria_type': 'sessions',
                'criteria_value': 10
            },
            {
                'name': '5 Hour Scholar',
                'description': 'Study for 5 hours total (300 minutes)',
                'icon': '🎓',
                'criteria_type': 'time',
                'criteria_value': 300
            }
        ]
        
        for badge_data in default_badges:
            # Check if badge already exists
            existing_badge = Badge.query.filter_by(name=badge_data['name']).first()
            if not existing_badge:
                badge = Badge(**badge_data)
                db.session.add(badge)
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating basic badges: {e}")
            return False
