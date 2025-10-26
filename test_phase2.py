#!/usr/bin/env python3
"""
Test script for Phase 2 database functionality
Demonstrates CRUD operations and business logic
"""

from app import app
from db_utils import *
from datetime import date

def test_phase2():
    """Test Phase 2 database functionality"""
    print("🧪 Testing Study Streak Motivator Phase 2 Database...")
    
    with app.app_context():
        # Test 1: Get the default user
        print("\n1️⃣ Testing user operations...")
        user = get_user_by_username('student')
        print(f"   Default user: {user.username} (ID: {user.id})")
        
        # Test 2: Create study sessions
        print("\n2️⃣ Creating test study sessions...")
        session1 = create_study_session(user.id, 'Math', 25)
        session2 = create_study_session(user.id, 'Science', 30)
        session3 = create_study_session(user.id, 'English', 20)
        print(f"   Created sessions: Math (25 min), Science (30 min), English (20 min)")
        
        # Test 3: Complete sessions and check for badges
        print("\n3️⃣ Completing sessions and checking badges...")
        completed_session, new_badges = complete_study_session(session1.id)
        print(f"   Completed {completed_session.subject} session")
        if new_badges:
            print(f"   🏆 New badges earned: {[badge.name for badge in new_badges]}")
        
        complete_study_session(session2.id)
        complete_study_session(session3.id)
        print("   Completed all sessions")
        
        # Test 4: Check streak
        print("\n4️⃣ Testing streak functionality...")
        current_streak = get_current_streak(user.id)
        if current_streak:
            print(f"   🔥 Current streak: {current_streak.current_days} days")
        else:
            print("   No active streak")
        
        # Test 5: Check badges
        print("\n5️⃣ Testing badge system...")
        earned_badges = get_user_badges(user.id)
        print(f"   🏆 Badges earned: {len(earned_badges)}")
        for badge in earned_badges:
            print(f"      - {badge.icon} {badge.name}: {badge.description}")
        
        # Test 6: Get dashboard data
        print("\n6️⃣ Testing dashboard data...")
        dashboard_data = get_dashboard_data(user.id)
        print(f"   Total study time: {dashboard_data['total_study_time']} minutes")
        print(f"   Total sessions: {dashboard_data['total_sessions']}")
        print(f"   Current streak: {dashboard_data['current_streak']} days")
        
        # Test 7: Subject statistics
        print("\n7️⃣ Subject breakdown:")
        for stat in dashboard_data['subject_stats']:
            print(f"   {stat['subject']}: {stat['total_minutes']} min ({stat['session_count']} sessions)")
        
        print("\n✅ Phase 2 database functionality test completed successfully!")
        print("\n📊 Database is ready for Phase 3 (Study Timer) implementation!")

if __name__ == "__main__":
    test_phase2()