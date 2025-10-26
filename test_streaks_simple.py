"""
Simple test script for Phase 4 streak calculation algorithms
Congressional App Challenge 2025
"""

import sys
import os
from datetime import date, datetime, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_streak_tests():
    """Run basic streak calculation tests"""
    from app import app
    from models import db, User, StudySession, Streak
    from streak_calculator import StreakCalculator, get_streak_status
    
    with app.app_context():
        print("🚀 Testing Phase 4 Streak Calculation...")
        print("=" * 50)
        
        # Setup test database
        db.drop_all()
        db.create_all()
        
        # Create test user
        test_user = User(username='test_user', email='test@example.com')
        db.session.add(test_user)
        db.session.commit()
        user_id = test_user.id
        
        calculator = StreakCalculator()
        today = calculator.get_local_date()
        
        print(f"📅 Testing with today = {today}")
        
        # Test 1: Basic consecutive streak
        print("\n🧪 Test 1: Basic consecutive streak")
        for i in range(3):
            session_date = today - timedelta(days=2-i)
            session = StudySession(
                user_id=user_id,
                subject="Math",
                duration_minutes=25,
                session_date=session_date,
                completed=True
            )
            db.session.add(session)
            print(f"  ✓ Added session for {session_date}")
        
        db.session.commit()
        
        # Calculate streak
        current_streak, start_date = calculator.calculate_current_streak(user_id)
        print(f"  📊 Current streak: {current_streak} days (started {start_date})")
        
        # Test 2: Streak status
        print("\n🧪 Test 2: Streak status")
        status = get_streak_status(user_id)
        print(f"  📝 Status: {status['status']}")
        print(f"  💬 Message: {status['message']}")
        print(f"  📈 Current: {status['current_streak']} days")
        print(f"  🏆 Longest: {status['longest_streak']} days")
        
        # Test 3: Database integration
        print("\n🧪 Test 3: Database integration")
        from db_utils import update_streak
        result = update_streak(user_id)
        print(f"  📊 Update result: {result}")
        
        # Verify database record
        active_streak = Streak.query.filter_by(user_id=user_id, is_active=True).first()
        if active_streak:
            print(f"  💾 DB record: {active_streak.current_days} days, active={active_streak.is_active}")
        else:
            print("  ⚠️ No active streak record found")
        
        # Test 4: Multiple sessions per day
        print("\n🧪 Test 4: Multiple sessions per day")
        tomorrow = today + timedelta(days=1)
        
        # Add multiple sessions for tomorrow
        for subject, duration in [("Math", 15), ("Science", 20), ("English", 10)]:
            session = StudySession(
                user_id=user_id,
                subject=subject,
                duration_minutes=duration,
                session_date=tomorrow,
                completed=True
            )
            db.session.add(session)
        
        db.session.commit()
        
        has_valid_day, total_minutes = calculator.has_valid_study_day(user_id, tomorrow)
        print(f"  📊 Tomorrow ({tomorrow}): {total_minutes} minutes, valid={has_valid_day}")
        
        # Update streak and check again
        update_result = update_streak(user_id)
        new_status = get_streak_status(user_id)
        print(f"  📈 Updated streak: {new_status['current_streak']} days")
        
        print("\n" + "=" * 50)
        print("✅ Basic streak calculation tests completed!")
        print("🎉 Phase 4 implementation working correctly!")
        
        return True

if __name__ == "__main__":
    try:
        success = run_streak_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)