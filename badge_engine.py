"""
Advanced Badge Engine for Study Streak Motivator
Phase 6 - Sophisticated badge checking and awarding system
Congressional App Challenge 2025
"""

import json
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple
from models import db, User, StudySession, Streak, Badge, UserBadge
from db_utils import get_total_study_time, get_user_sessions
from streak_calculator import get_current_streak


class BadgeEngine:
    """
    Advanced badge engine that handles complex badge criteria and awarding logic
    """
    
    def __init__(self):
        self.badge_checkers = {
            'sessions': self.check_session_badges,
            'streak': self.check_streak_badges,
            'time': self.check_time_badges,
            'subject_time': self.check_subject_time_badges,
            'special': self.check_special_badges
        }
    
    def check_and_award_badges(self, user_id: int, trigger_event: str = 'session_complete') -> List[Badge]:
        """
        Check for newly earned badges and award them
        
        Args:
            user_id: User to check badges for
            trigger_event: What triggered the badge check (session_complete, streak_update, etc.)
            
        Returns:
            List of newly earned badges
        """
        user = User.query.get(user_id)
        if not user:
            return []
        
        # Get badges user hasn't earned yet
        earned_badge_ids = [ub.badge_id for ub in user.user_badges]
        available_badges = Badge.query.filter(
            ~Badge.id.in_(earned_badge_ids),
            Badge.is_active == True
        ).all()
        
        newly_earned = []
        
        for badge in available_badges:
            if self.is_badge_earned(user_id, badge):
                # Award the badge
                user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                db.session.add(user_badge)
                newly_earned.append(badge)
        
        # Check for meta-achievements (badges that depend on other badges)
        meta_badges = self.check_meta_achievements(user_id, newly_earned)
        newly_earned.extend(meta_badges)
        
        try:
            db.session.commit()
            return newly_earned
        except Exception as e:
            db.session.rollback()
            print(f"Error awarding badges: {e}")
            return []
    
    def is_badge_earned(self, user_id: int, badge: Badge) -> bool:
        """
        Check if a specific badge has been earned
        
        Args:
            user_id: User to check
            badge: Badge to check for
            
        Returns:
            True if badge is earned, False otherwise
        """
        checker_func = self.badge_checkers.get(badge.criteria_type)
        if not checker_func:
            print(f"Unknown badge criteria type: {badge.criteria_type}")
            return False
        
        return checker_func(user_id, badge)
    
    def check_session_badges(self, user_id: int, badge: Badge) -> bool:
        """Check badges based on session count"""
        session_count = StudySession.query.filter_by(
            user_id=user_id,
            completed=True
        ).count()
        
        return session_count >= badge.criteria_value
    
    def check_streak_badges(self, user_id: int, badge: Badge) -> bool:
        """Check badges based on study streaks"""
        current_streak = get_current_streak(user_id)
        if not current_streak:
            return False
        
        return current_streak.current_days >= badge.criteria_value
    
    def check_time_badges(self, user_id: int, badge: Badge) -> bool:
        """Check badges based on total study time"""
        total_time = get_total_study_time(user_id)
        return total_time >= badge.criteria_value
    
    def check_subject_time_badges(self, user_id: int, badge: Badge) -> bool:
        """Check badges based on time spent on specific subjects"""
        criteria_details = badge.get_criteria_details()
        subject = criteria_details.get('subject')
        
        if not subject:
            return False
        
        # Calculate total time for this subject
        sessions = StudySession.query.filter_by(
            user_id=user_id,
            subject=subject,
            completed=True
        ).all()
        
        subject_time = sum(session.duration_minutes for session in sessions if session.duration_minutes)
        return subject_time >= badge.criteria_value
    
    def check_special_badges(self, user_id: int, badge: Badge) -> bool:
        """Check special achievement badges with complex criteria"""
        criteria_details = badge.get_criteria_details()
        condition = criteria_details.get('condition')
        
        if condition == 'study_after_hour':
            return self.check_time_of_day_sessions(user_id, criteria_details.get('hour'), 'after', badge.criteria_value)
        
        elif condition == 'study_before_hour':
            return self.check_time_of_day_sessions(user_id, criteria_details.get('hour'), 'before', badge.criteria_value)
        
        elif condition == 'weekend_sessions':
            return self.check_weekend_sessions(user_id, badge.criteria_value)
        
        elif condition == 'single_session_duration':
            return self.check_long_session(user_id, badge.criteria_value)
        
        elif condition == 'subjects_in_week':
            subjects = criteria_details.get('subjects', [])
            return self.check_subjects_in_timeframe(user_id, subjects, 7)
        
        elif condition == 'earn_all_badges':
            rarities = criteria_details.get('rarities', [])
            return self.check_earned_all_badges_by_rarity(user_id, rarities)
        
        return False
    
    def check_time_of_day_sessions(self, user_id: int, hour: int, comparison: str, required_count: int) -> bool:
        """Check if user has studied at specific times"""
        sessions = StudySession.query.filter_by(
            user_id=user_id,
            completed=True
        ).filter(StudySession.start_time.isnot(None)).all()
        
        count = 0
        for session in sessions:
            session_hour = session.start_time.hour
            
            if comparison == 'after' and session_hour >= hour:
                count += 1
            elif comparison == 'before' and session_hour <= hour:
                count += 1
        
        return count >= required_count
    
    def check_weekend_sessions(self, user_id: int, required_weekends: int) -> bool:
        """Check if user has studied on multiple weekends"""
        sessions = StudySession.query.filter_by(
            user_id=user_id,
            completed=True
        ).all()
        
        weekend_dates = set()
        for session in sessions:
            # Check if session was on weekend (Saturday=5, Sunday=6)
            if session.session_date.weekday() in [5, 6]:
                # Get the Saturday of this weekend
                days_since_saturday = (session.session_date.weekday() + 2) % 7
                weekend_start = session.session_date - timedelta(days=days_since_saturday)
                weekend_dates.add(weekend_start)
        
        return len(weekend_dates) >= required_weekends
    
    def check_long_session(self, user_id: int, required_duration: int) -> bool:
        """Check if user has completed a session of required duration"""
        longest_session = StudySession.query.filter_by(
            user_id=user_id,
            completed=True
        ).filter(StudySession.duration_minutes >= required_duration).first()
        
        return longest_session is not None
    
    def check_subjects_in_timeframe(self, user_id: int, subjects: List[str], days: int) -> bool:
        """Check if user studied all subjects within timeframe"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        # Get sessions in the timeframe
        sessions = StudySession.query.filter(
            StudySession.user_id == user_id,
            StudySession.completed == True,
            StudySession.session_date >= start_date,
            StudySession.session_date <= end_date
        ).all()
        
        studied_subjects = set(session.subject for session in sessions)
        required_subjects = set(subjects)
        
        return required_subjects.issubset(studied_subjects)
    
    def check_earned_all_badges_by_rarity(self, user_id: int, rarities: List[str]) -> bool:
        """Check if user has earned all badges of specified rarities"""
        # Get all badges of specified rarities
        target_badges = Badge.query.filter(
            Badge.rarity.in_(rarities),
            Badge.is_active == True,
            Badge.is_secret == False  # Don't count secret badges
        ).all()
        
        # Get badges user has earned
        earned_badges = db.session.query(Badge).join(UserBadge).filter(
            UserBadge.user_id == user_id,
            Badge.rarity.in_(rarities)
        ).all()
        
        return len(earned_badges) >= len(target_badges)
    
    def check_meta_achievements(self, user_id: int, newly_earned: List[Badge]) -> List[Badge]:
        """Check for meta-achievements that might be unlocked by earning other badges"""
        meta_badges = []
        
        # Check if user just earned enough badges to unlock meta achievements
        earned_badge_ids = [ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).all()]
        available_meta_badges = Badge.query.filter(
            ~Badge.id.in_(earned_badge_ids),
            Badge.criteria_type == 'special',
            Badge.is_active == True
        ).all()
        
        for badge in available_meta_badges:
            criteria_details = badge.get_criteria_details()
            condition = criteria_details.get('condition')
            
            if condition == 'earn_all_badges':
                if self.check_earned_all_badges_by_rarity(user_id, criteria_details.get('rarities', [])):
                    user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                    db.session.add(user_badge)
                    meta_badges.append(badge)
        
        return meta_badges
    
    def get_badge_progress(self, user_id: int, badge: Badge) -> Dict:
        """
        Get progress toward earning a specific badge
        
        Args:
            user_id: User to check progress for
            badge: Badge to check progress toward
            
        Returns:
            Dictionary with progress information
        """
        progress = {
            'badge_id': badge.id,
            'badge_name': badge.name,
            'current': 0,
            'required': badge.criteria_value,
            'progress_percent': 0,
            'description': badge.description,
            'is_earned': False
        }
        
        # Check if already earned
        user_badge = UserBadge.query.filter_by(user_id=user_id, badge_id=badge.id).first()
        if user_badge:
            progress['is_earned'] = True
            progress['progress_percent'] = 100
            return progress
        
        # Calculate current progress based on badge type
        if badge.criteria_type == 'sessions':
            progress['current'] = StudySession.query.filter_by(user_id=user_id, completed=True).count()
        
        elif badge.criteria_type == 'streak':
            current_streak = get_current_streak(user_id)
            progress['current'] = current_streak.current_days if current_streak else 0
        
        elif badge.criteria_type == 'time':
            progress['current'] = get_total_study_time(user_id)
        
        elif badge.criteria_type == 'subject_time':
            criteria_details = badge.get_criteria_details()
            subject = criteria_details.get('subject')
            if subject:
                sessions = StudySession.query.filter_by(
                    user_id=user_id,
                    subject=subject,
                    completed=True
                ).all()
                progress['current'] = sum(session.duration_minutes for session in sessions if session.duration_minutes)
        
        elif badge.criteria_type == 'special':
            # Special badges have complex progress calculation
            progress['current'] = self.get_special_badge_progress(user_id, badge)
        
        # Calculate progress percentage
        if progress['required'] > 0:
            progress['progress_percent'] = min(100, (progress['current'] / progress['required']) * 100)
        
        return progress
    
    def get_special_badge_progress(self, user_id: int, badge: Badge) -> int:
        """Get progress for special badges with complex criteria"""
        criteria_details = badge.get_criteria_details()
        condition = criteria_details.get('condition')
        
        if condition in ['study_after_hour', 'study_before_hour']:
            hour = criteria_details.get('hour')
            comparison = 'after' if condition == 'study_after_hour' else 'before'
            
            sessions = StudySession.query.filter_by(
                user_id=user_id,
                completed=True
            ).filter(StudySession.start_time.isnot(None)).all()
            
            count = 0
            for session in sessions:
                session_hour = session.start_time.hour
                if comparison == 'after' and session_hour >= hour:
                    count += 1
                elif comparison == 'before' and session_hour <= hour:
                    count += 1
            
            return count
        
        elif condition == 'weekend_sessions':
            sessions = StudySession.query.filter_by(user_id=user_id, completed=True).all()
            weekend_dates = set()
            for session in sessions:
                if session.session_date.weekday() in [5, 6]:
                    days_since_saturday = (session.session_date.weekday() + 2) % 7
                    weekend_start = session.session_date - timedelta(days=days_since_saturday)
                    weekend_dates.add(weekend_start)
            return len(weekend_dates)
        
        elif condition == 'single_session_duration':
            longest = StudySession.query.filter_by(
                user_id=user_id,
                completed=True
            ).order_by(StudySession.duration_minutes.desc()).first()
            return longest.duration_minutes if longest else 0
        
        return 0


# Global badge engine instance
badge_engine = BadgeEngine()


def check_and_award_badges(user_id: int, trigger_event: str = 'session_complete') -> List[Badge]:
    """Convenience function for checking and awarding badges"""
    return badge_engine.check_and_award_badges(user_id, trigger_event)


def get_badge_progress_for_user(user_id: int) -> List[Dict]:
    """Get progress toward all available badges for a user"""
    earned_badge_ids = [ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).all()]
    
    # Get unearned badges (excluding secret ones)
    available_badges = Badge.query.filter(
        ~Badge.id.in_(earned_badge_ids),
        Badge.is_active == True,
        Badge.is_secret == False
    ).order_by(Badge.tier, Badge.rarity).all()
    
    progress_list = []
    for badge in available_badges:
        progress = badge_engine.get_badge_progress(user_id, badge)
        progress_list.append(progress)
    
    return progress_list