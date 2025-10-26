"""
Advanced Streak Calculation Module for Study Streak Motivator
Phase 4 Implementation - Robust streak algorithms with timezone support
Congressional App Challenge 2025
"""

from datetime import date, datetime, timedelta
from dateutil import tz
from models import db, User, StudySession, Streak
from typing import Optional, Tuple, Dict, List

# Configuration Constants
MIN_STUDY_MINUTES = 5  # Minimum minutes for a session to count toward streak
STREAK_TIMEZONE = 'America/New_York'  # Default timezone for streak calculations


class StreakCalculator:
    """
    Advanced streak calculation engine with timezone support and robust algorithms
    """
    
    def __init__(self, timezone_name: str = STREAK_TIMEZONE):
        """
        Initialize streak calculator with timezone
        
        Args:
            timezone_name: Timezone name (e.g. 'America/New_York')
        """
        self.timezone = tz.gettz(timezone_name)
        self.min_study_minutes = MIN_STUDY_MINUTES
    
    def get_local_date(self, dt: datetime = None) -> date:
        """
        Get current date in the configured timezone
        
        Args:
            dt: Optional datetime to convert, defaults to now
            
        Returns:
            Date in configured timezone
        """
        if dt is None:
            dt = datetime.utcnow()
        
        # Convert UTC to local timezone
        local_dt = dt.replace(tzinfo=tz.UTC).astimezone(self.timezone)
        return local_dt.date()
    
    def has_valid_study_day(self, user_id: int, target_date: date) -> Tuple[bool, int]:
        """
        Check if user has valid study sessions on a specific date
        
        Args:
            user_id: User ID to check
            target_date: Date to check for study sessions
            
        Returns:
            Tuple of (has_valid_sessions, total_study_minutes)
        """
        sessions = StudySession.query.filter_by(
            user_id=user_id,
            session_date=target_date,
            completed=True
        ).all()
        
        total_minutes = sum(
            session.duration_minutes 
            for session in sessions 
            if session.duration_minutes and session.duration_minutes >= self.min_study_minutes
        )
        
        return total_minutes >= self.min_study_minutes, total_minutes
    
    def calculate_current_streak(self, user_id: int) -> Tuple[int, Optional[date]]:
        """
        Calculate the user's current active streak
        
        Args:
            user_id: User ID to calculate streak for
            
        Returns:
            Tuple of (streak_days, streak_start_date)
        """
        today = self.get_local_date()
        current_streak_days = 0
        streak_start_date = None
        
        # Check backwards from today to find consecutive study days
        check_date = today
        while True:
            has_valid_day, _ = self.has_valid_study_day(user_id, check_date)
            
            if has_valid_day:
                current_streak_days += 1
                streak_start_date = check_date
                check_date -= timedelta(days=1)
            else:
                break
        
        # If no study today, check if yesterday was studied (grace period)
        if current_streak_days == 0:
            yesterday = today - timedelta(days=1)
            has_yesterday, _ = self.has_valid_study_day(user_id, yesterday)
            
            if has_yesterday:
                # Start from yesterday and count backwards
                current_streak_days = 1
                streak_start_date = yesterday
                check_date = yesterday - timedelta(days=1)
                
                while True:
                    has_valid_day, _ = self.has_valid_study_day(user_id, check_date)
                    if has_valid_day:
                        current_streak_days += 1
                        streak_start_date = check_date
                        check_date -= timedelta(days=1)
                    else:
                        break
        
        return current_streak_days, streak_start_date
    
    def calculate_longest_streak(self, user_id: int) -> Tuple[int, Optional[date], Optional[date]]:
        """
        Calculate the user's longest streak ever
        
        Args:
            user_id: User ID to calculate for
            
        Returns:
            Tuple of (longest_streak_days, start_date, end_date)
        """
        # Get all completed study sessions ordered by date
        sessions = db.session.query(StudySession.session_date).filter_by(
            user_id=user_id,
            completed=True
        ).filter(
            StudySession.duration_minutes >= self.min_study_minutes
        ).group_by(StudySession.session_date).order_by(StudySession.session_date).all()
        
        if not sessions:
            return 0, None, None
        
        study_dates = [session[0] for session in sessions]
        
        longest_streak = 0
        longest_start = None
        longest_end = None
        
        current_streak = 1
        current_start = study_dates[0]
        
        for i in range(1, len(study_dates)):
            current_date = study_dates[i]
            previous_date = study_dates[i-1]
            
            # Check if dates are consecutive
            if current_date == previous_date + timedelta(days=1):
                current_streak += 1
            else:
                # Current streak ended, check if it's the longest
                if current_streak > longest_streak:
                    longest_streak = current_streak
                    longest_start = current_start
                    longest_end = study_dates[i-1]
                
                # Start new streak
                current_streak = 1
                current_start = current_date
        
        # Check final streak
        if current_streak > longest_streak:
            longest_streak = current_streak
            longest_start = current_start
            longest_end = study_dates[-1]
        
        return longest_streak, longest_start, longest_end
    
    def update_user_streak(self, user_id: int) -> Dict:
        """
        Update user's streak after a study session
        
        Args:
            user_id: User ID to update
            
        Returns:
            Dictionary with streak update information
        """
        current_streak_days, streak_start = self.calculate_current_streak(user_id)
        longest_streak_days, longest_start, longest_end = self.calculate_longest_streak(user_id)
        
        # Get or create current streak record
        active_streak = Streak.query.filter_by(user_id=user_id, is_active=True).first()
        
        if current_streak_days == 0:
            # No current streak - mark existing as inactive
            if active_streak:
                active_streak.is_active = False
                active_streak.end_date = self.get_local_date() - timedelta(days=1)
                db.session.commit()
            
            return {
                'current_streak': 0,
                'longest_streak': longest_streak_days,
                'streak_broken': active_streak is not None,
                'new_record': False
            }
        
        # There is a current streak
        if active_streak:
            # Update existing streak
            active_streak.current_days = current_streak_days
            active_streak.start_date = streak_start
        else:
            # Create new streak
            active_streak = Streak(
                user_id=user_id,
                start_date=streak_start,
                current_days=current_streak_days,
                is_active=True
            )
            db.session.add(active_streak)
        
        db.session.commit()
        
        # Check if this is a new personal record
        new_record = current_streak_days > longest_streak_days
        
        return {
            'current_streak': current_streak_days,
            'longest_streak': max(longest_streak_days, current_streak_days),
            'streak_broken': False,
            'new_record': new_record,
            'streak_start_date': streak_start.isoformat() if streak_start else None
        }
    
    def get_streak_status(self, user_id: int) -> Dict:
        """
        Get comprehensive streak status for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with complete streak information
        """
        today = self.get_local_date()
        has_studied_today, today_minutes = self.has_valid_study_day(user_id, today)
        has_studied_yesterday, _ = self.has_valid_study_day(user_id, today - timedelta(days=1))
        
        current_streak_days, streak_start = self.calculate_current_streak(user_id)
        longest_streak_days, longest_start, longest_end = self.calculate_longest_streak(user_id)
        
        # Determine streak status
        if current_streak_days == 0:
            if has_studied_yesterday:
                status = "broken_today"
                message = "Your streak was broken! Study today to start a new one."
            else:
                status = "no_streak"
                message = "No active streak. Start studying to begin your streak!"
        elif has_studied_today:
            status = "active_studied_today"
            message = f"Great job! You're on a {current_streak_days}-day streak!"
        else:
            status = "at_risk"
            message = f"You're on a {current_streak_days}-day streak. Study today to keep it going!"
        
        return {
            'current_streak': current_streak_days,
            'longest_streak': longest_streak_days,
            'streak_start_date': streak_start.isoformat() if streak_start else None,
            'longest_streak_start': longest_start.isoformat() if longest_start else None,
            'longest_streak_end': longest_end.isoformat() if longest_end else None,
            'status': status,
            'message': message,
            'has_studied_today': has_studied_today,
            'today_study_minutes': today_minutes,
            'is_new_record': current_streak_days > 0 and current_streak_days == longest_streak_days
        }
    
    def get_streak_calendar_data(self, user_id: int, year: int = None, month: int = None) -> Dict:
        """
        Get streak data for calendar visualization
        
        Args:
            user_id: User ID
            year: Year to get data for (defaults to current year)
            month: Month to get data for (defaults to current month)
            
        Returns:
            Dictionary with calendar data
        """
        if year is None:
            year = self.get_local_date().year
        if month is None:
            month = self.get_local_date().month
        
        # Get first and last day of the month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        calendar_data = {}
        current_date = first_day
        
        while current_date <= last_day:
            has_valid_day, total_minutes = self.has_valid_study_day(user_id, current_date)
            
            calendar_data[current_date.isoformat()] = {
                'has_streak_activity': has_valid_day,
                'total_study_minutes': total_minutes,
                'is_today': current_date == self.get_local_date()
            }
            
            current_date += timedelta(days=1)
        
        return calendar_data


# Global instance for easy access
streak_calculator = StreakCalculator()


# Convenience functions for backward compatibility
def update_streak(user_id: int) -> Dict:
    """Update user streak (backward compatible)"""
    return streak_calculator.update_user_streak(user_id)


def get_current_streak(user_id: int) -> Optional[Streak]:
    """Get current streak model (backward compatible)"""
    return Streak.query.filter_by(user_id=user_id, is_active=True).first()


def get_streak_status(user_id: int) -> Dict:
    """Get comprehensive streak status"""
    return streak_calculator.get_streak_status(user_id)


def get_streak_calendar_data(user_id: int, year: int = None, month: int = None) -> Dict:
    """Get calendar data for streak visualization"""
    return streak_calculator.get_streak_calendar_data(user_id, year, month)