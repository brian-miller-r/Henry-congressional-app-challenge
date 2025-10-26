#!/usr/bin/env python3
"""
Create sample data for testing the Study Streak Motivator web interface
"""

from app import app
from db_utils import *
from datetime import date, timedelta
import random

def create_sample_data():
    """Create realistic sample data for testing"""
    print("🎭 Creating sample data for Study Streak Motivator...")
    
    with app.app_context():
        user = get_user_by_username('student')
        if not user:
            print("❌ Default user not found. Please run init_db.py first.")
            return
        
        print(f"👤 Using user: {user.username} (ID: {user.id})")
        
        # Create study sessions over the past week
        subjects = ['Math', 'Science', 'English', 'History', 'Other']
        durations = [15, 20, 25, 30, 45]  # Common study session lengths
        
        # Create sessions for the past 7 days to build up a streak
        sessions_created = 0
        for days_ago in range(7, 0, -1):  # 7 days ago to yesterday
            session_date = date.today() - timedelta(days=days_ago)
            
            # Create 1-3 sessions per day
            daily_sessions = random.randint(1, 3)
            for _ in range(daily_sessions):
                subject = random.choice(subjects)
                duration = random.choice(durations)
                
                session = create_study_session(
                    user.id, 
                    subject, 
                    duration, 
                    session_date
                )
                # Mark as completed
                session.mark_completed()
                sessions_created += 1
        
        # Create sessions for today
        today_sessions = 2
        for _ in range(today_sessions):
            subject = random.choice(subjects)
            duration = random.choice(durations)
            
            session = create_study_session(user.id, subject, duration)
            session.mark_completed()
            sessions_created += 1
        
        print(f"📚 Created {sessions_created} study sessions over 8 days")
        
        # Update streak calculations
        print("🔥 Updating streak data...")
        current_streak = update_streak(user.id)
        if current_streak:
            print(f"   Current streak: {current_streak.current_days} days")
        
        # Check for badges
        print("🏆 Checking for badge awards...")
        new_badges = check_and_award_badges(user.id)
        if new_badges:
            print(f"   New badges awarded: {[badge.name for badge in new_badges]}")
        else:
            print("   No new badges awarded")
        
        # Show final stats
        print("\n📊 Sample Data Summary:")
        dashboard_data = get_dashboard_data(user.id)
        
        print(f"   Total study time: {dashboard_data['total_study_time']} minutes")
        print(f"   Weekly study time: {dashboard_data['weekly_study_time']} minutes")
        print(f"   Total sessions: {dashboard_data['total_sessions']}")
        print(f"   Current streak: {dashboard_data['current_streak']} days")
        print(f"   Badges earned: {len(dashboard_data['earned_badges'])}")
        
        if dashboard_data['subject_stats']:
            print(f"\n   📖 Subject breakdown:")
            for stat in dashboard_data['subject_stats']:
                print(f"      {stat['subject']}: {stat['total_minutes']} min ({stat['session_count']} sessions)")
        
        if dashboard_data['earned_badges']:
            print(f"\n   🏆 Earned badges:")
            for badge in dashboard_data['earned_badges']:
                print(f"      {badge.icon} {badge.name}")
        
        print(f"\n✅ Sample data created successfully!")
        print(f"🌐 Visit http://127.0.0.1:5004/dashboard to see the data!")

if __name__ == "__main__":
    create_sample_data()