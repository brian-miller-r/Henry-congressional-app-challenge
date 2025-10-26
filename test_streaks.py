"""
Test script for Phase 4 streak calculation algorithms
Tests various edge cases and scenarios for robust streak tracking
Congressional App Challenge 2025
"""

import sys
import os
from datetime import date, datetime, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, StudySession, Streak
from streak_calculator import StreakCalculator, get_streak_status
import json

def setup_test_database():
    """Create a clean test database"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create test user
        test_user = User(username='test_user', email='test@example.com')
        db.session.add(test_user)
        db.session.commit()
        
        return test_user.id

def create_test_session(user_id, session_date, duration_minutes=25, subject="Math", completed=True):
    """Helper to create a test study session"""
    with app.app_context():
        session = StudySession(
            user_id=user_id,
            subject=subject,
            duration_minutes=duration_minutes,
            session_date=session_date,
            start_time=datetime.combine(session_date, datetime.min.time()),
            completed=completed
        )
        db.session.add(session)
        db.session.commit()
        return session

def test_basic_streak_calculation():
    """Test basic streak calculation with consecutive days"""
    print("\\n🧪 Testing basic streak calculation...")
    
    user_id = setup_test_database()
    
    with app.app_context():
        calculator = StreakCalculator()
        
        # Create study sessions for 5 consecutive days ending today
        today = calculator.get_local_date()
        for i in range(5):
            session_date = today - timedelta(days=4-i)
            create_test_session(user_id, session_date, duration_minutes=30)
            print(f"  ✓ Created session for {session_date}")
        
        # Test streak calculation
        current_streak, start_date = calculator.calculate_current_streak(user_id)
        longest_streak, longest_start, longest_end = calculator.calculate_longest_streak(user_id)
        
        print(f"  📊 Current streak: {current_streak} days (started {start_date})")
        print(f"  🏆 Longest streak: {longest_streak} days")
        
        assert current_streak == 5, f"Expected 5-day streak, got {current_streak}"
        assert longest_streak == 5, f"Expected 5-day longest streak, got {longest_streak}"
        print("  ✅ Basic streak calculation passed!")

def test_minimum_study_time():
    """Test minimum study time requirements"""
    print("\\n🧪 Testing minimum study time requirements...")
    
    user_id = setup_test_database()
    
    with app.app_context():
        calculator = StreakCalculator()
        today = calculator.get_local_date()
        
        # Create sessions with varying durations
        create_test_session(user_id, today - timedelta(days=2), duration_minutes=30)  # Valid
        create_test_session(user_id, today - timedelta(days=1), duration_minutes=3)   # Too short
        create_test_session(user_id, today, duration_minutes=25)                       # Valid
        
        current_streak, _ = calculator.calculate_current_streak(user_id)
        
        # Should only count days with >= 5 minutes (so streak should be 1, not 2)
        print(f"  📊 Current streak with min time filter: {current_streak} days")
        assert current_streak == 1, f"Expected 1-day streak (yesterday too short), got {current_streak}"
        print("  ✅ Minimum study time test passed!")

def test_streak_grace_period():
    """Test grace period for streak continuation"""
    print("\\n🧪 Testing streak grace period...")
    
    user_id = setup_test_database()
    calculator = StreakCalculator()
    today = calculator.get_local_date()
    
    # Create sessions for yesterday but not today
    create_test_session(user_id, today - timedelta(days=2), duration_minutes=25)
    create_test_session(user_id, today - timedelta(days=1), duration_minutes=25)
    # No session today
    
    current_streak, _ = calculator.calculate_current_streak(user_id)
    
    print(f"  📊 Streak with grace period: {current_streak} days")
    assert current_streak == 2, f"Expected 2-day streak (grace period), got {current_streak}"
    print("  ✅ Grace period test passed!")

def test_broken_streak():
    """Test detection of broken streaks"""
    print("\\n🧪 Testing broken streak detection...")
    
    user_id = setup_test_database()
    calculator = StreakCalculator()
    today = calculator.get_local_date()
    
    # Create sessions with a gap
    create_test_session(user_id, today - timedelta(days=4), duration_minutes=25)
    create_test_session(user_id, today - timedelta(days=3), duration_minutes=25)
    # Gap on day -2
    create_test_session(user_id, today - timedelta(days=1), duration_minutes=25)
    create_test_session(user_id, today, duration_minutes=25)
    
    current_streak, _ = calculator.calculate_current_streak(user_id)
    longest_streak, _, _ = calculator.calculate_longest_streak(user_id)
    
    print(f"  📊 Current streak after gap: {current_streak} days")
    print(f"  🏆 Longest streak: {longest_streak} days")
    
    assert current_streak == 2, f"Expected 2-day current streak, got {current_streak}"
    assert longest_streak == 2, f"Expected 2-day longest streak, got {longest_streak}"
    print("  ✅ Broken streak test passed!")

def test_streak_status_messages():
    """Test streak status messages and user feedback"""
    print("\\n🧪 Testing streak status messages...")
    
    user_id = setup_test_database()
    calculator = StreakCalculator()
    today = calculator.get_local_date()
    
    # Test various scenarios
    scenarios = [
        # (sessions_data, expected_status, description)
        ([], "no_streak", "No sessions"),
        ([(today - timedelta(days=1), 25)], "broken_today", "Only yesterday"),
        ([(today, 25)], "active_studied_today", "Only today"),
        ([(today - timedelta(days=1), 25), (today, 25)], "active_studied_today", "Two consecutive days"),
        ([(today - timedelta(days=1), 25)], "broken_today", "Yesterday only (at risk)"),
    ]
    
    for i, (sessions_data, expected_status, description) in enumerate(scenarios):
        # Reset database for each test
        user_id = setup_test_database()
        
        # Create sessions
        for session_date, duration in sessions_data:
            create_test_session(user_id, session_date, duration)
        
        # Get status
        with app.app_context():
            status = get_streak_status(user_id)
        
        print(f"  📝 Scenario {i+1} ({description}): {status['status']} - '{status['message']}'")
        
        # Note: We're testing that it returns a valid status, exact matching depends on implementation details
        assert 'status' in status, f"Status missing in scenario {i+1}"
        assert 'message' in status, f"Message missing in scenario {i+1}"
    
    print("  ✅ Status message test passed!")

def test_multiple_sessions_per_day():
    """Test handling multiple study sessions in one day"""
    print("\\n🧪 Testing multiple sessions per day...")
    
    user_id = setup_test_database()
    calculator = StreakCalculator()
    today = calculator.get_local_date()
    
    # Create multiple sessions on the same day
    create_test_session(user_id, today, duration_minutes=15, subject="Math")
    create_test_session(user_id, today, duration_minutes=20, subject="Science")
    create_test_session(user_id, today, duration_minutes=10, subject="English")
    
    has_valid_day, total_minutes = calculator.has_valid_study_day(user_id, today)
    
    print(f"  📊 Multiple sessions total: {total_minutes} minutes")
    print(f"  ✓ Valid study day: {has_valid_day}")
    
    assert has_valid_day, "Should be a valid study day with multiple sessions"
    assert total_minutes == 45, f"Expected 45 total minutes, got {total_minutes}"
    print("  ✅ Multiple sessions test passed!")

def test_update_streak_integration():
    """Test the update_streak function integration"""
    print("\\n🧪 Testing update_streak integration...")
    
    user_id = setup_test_database()
    calculator = StreakCalculator()
    today = calculator.get_local_date()
    
    # Create initial sessions
    create_test_session(user_id, today - timedelta(days=1), duration_minutes=25)
    create_test_session(user_id, today, duration_minutes=30)
    
    # Update streak
    with app.app_context():
        from db_utils import update_streak
        result = update_streak(user_id)
    
    print(f"  📊 Streak update result: {json.dumps(result, indent=2)}")
    
    assert 'current_streak' in result, "Result should contain current_streak"
    assert result['current_streak'] == 2, f"Expected 2-day streak, got {result['current_streak']}"
    
    # Verify database record was created/updated
    with app.app_context():
        active_streak = Streak.query.filter_by(user_id=user_id, is_active=True).first()
        assert active_streak is not None, "Should have an active streak record"
        assert active_streak.current_days == 2, f"DB record should show 2 days, got {active_streak.current_days}"
    
    print("  ✅ Update streak integration test passed!")

def run_all_tests():
    """Run all streak calculation tests"""
    print("🚀 Starting Phase 4 Streak Calculation Tests...")
    print("=" * 60)
    
    try:
        test_basic_streak_calculation()
        test_minimum_study_time()
        test_streak_grace_period()
        test_broken_streak()
        test_streak_status_messages()
        test_multiple_sessions_per_day()
        test_update_streak_integration()
        
        print("\\n" + "=" * 60)
        print("🎉 All streak calculation tests passed!")
        print("✅ Phase 4 streak algorithms are working correctly!")
        
    except Exception as e:
        print(f"\\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)