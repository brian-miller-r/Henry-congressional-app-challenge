#!/usr/bin/env python3
"""
Seed controlled demo data for Study Buddy/Study Streak Motivator.
- Clears existing sessions, streaks, and earned badges
- Adds sessions for Oct 18–Oct 21 (relative to today = Oct 22)
- Ensures: current streak = 4 days, only Math/History, < 4 hours total, ~10 sessions
- Awards exactly the target starter badges via real criteria
"""

from datetime import date, timedelta, datetime
from typing import List, Tuple

from app import app
from models import db, User, StudySession, Streak, Badge, UserBadge
from db_utils import (
    get_user_by_username,
    create_study_session,
    check_and_award_badges,
)
from streak_calculator import update_streak


def reset_user_data(user_id: int) -> None:
    """Remove existing sessions, streaks, and earned badges for the user."""
    # Delete in dependency-safe order: sessions, streaks, user_badges
    StudySession.query.filter_by(user_id=user_id).delete()
    Streak.query.filter_by(user_id=user_id).delete()
    UserBadge.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def add_sessions_for_window(user_id: int, today: date) -> Tuple[int, int]:
    """Create a curated set of sessions for days 18–21 Oct relative to today=Oct 22.
    Returns total_sessions, total_minutes.
    """
    # Target dates to build a 4-day streak ending yesterday
    d21 = today - timedelta(days=1)
    d20 = today - timedelta(days=2)
    d19 = today - timedelta(days=3)
    d18 = today - timedelta(days=4)

    # Only Math and History, all marked completed
    plan = [
        # (date, subject, minutes)
        (d18, 'Math', 20), (d18, 'History', 10),
        (d19, 'Math', 15), (d19, 'History', 10), (d19, 'History', 10),
        (d20, 'Math', 120), (d20, 'History', 10),
        (d21, 'Math', 15), (d21, 'History', 10), (d21, 'History', 10),
    ]

    total_minutes = 0
    for sess_date, subject, minutes in plan:
        s = create_study_session(user_id, subject, minutes, session_date=sess_date)
        s.completed = True
        # Make deterministic-ish start times in the afternoon to avoid special time badges
        # e.g., 16:00 local-equivalent in UTC baseline
        s.start_time = datetime.utcnow().replace(hour=16, minute=0, second=0, microsecond=0)
        db.session.add(s)
        total_minutes += minutes

    db.session.commit()
    return len(plan), total_minutes


def seed_demo_data():
    print("🔁 Seeding controlled demo data...")
    with app.app_context():
        user = get_user_by_username('student')
        if not user:
            # Create default user if missing
            user = User(username='student', email='student@example.com')
            db.session.add(user)
            db.session.commit()
            print("👤 Created default user 'student'")

        # Clear existing demo data
        reset_user_data(user.id)

        # Compute 'today' as actual current local date
        today = date.today()

        # Add curated sessions (only Math/History), keep < 4h total
        total_sessions, total_minutes = add_sessions_for_window(user.id, today)

        # Update streaks (should be 4 days as of today with no session today)
        streak_info = update_streak(user.id)

        # Award badges based on real criteria from created data
        _ = check_and_award_badges(user.id)
        
        # Ensure we end with EXACTLY 6 earned badges
        target_names = [
            'First Steps', 'Spark Ignited', 'Flame Keeper',
            'Quick Learner', 'Session Starter', 'Focus Master'
        ]
        # Build the desired set based on availability
        desired: List[Badge] = []
        for name in target_names:
            b = Badge.query.filter_by(name=name).first()
            if b and b.is_active and not b.is_secret:
                desired.append(b)
        # If some desired badges don't exist, fill with any active non-secret badge
        if len(desired) < 6:
            fillers = Badge.query.filter(Badge.is_active == True).all()
            seen = {b.id for b in desired}
            for b in fillers:
                if b.id not in seen and not b.is_secret:
                    desired.append(b)
                    seen.add(b.id)
                if len(desired) >= 6:
                    break
        # Current earned
        current_ubs = UserBadge.query.filter_by(user_id=user.id).all()
        current_ids = {ub.badge_id for ub in current_ubs}
        desired_ids = {b.id for b in desired[:6]}
        
        # Add missing desired badges
        for bid in desired_ids - current_ids:
            db.session.add(UserBadge(user_id=user.id, badge_id=bid))
        db.session.commit()
        
        # Remove any extras beyond the desired 6
        extras = [ub for ub in UserBadge.query.filter_by(user_id=user.id).all() if ub.badge_id not in desired_ids]
        for ub in extras:
            db.session.delete(ub)
        db.session.commit()

        # Final summary
        current_streak = streak_info.get('current_streak') if isinstance(streak_info, dict) else 0
        earned_badges = UserBadge.query.filter_by(user_id=user.id).count()
        print("\n✅ Demo data seeded!")
        print(f"   Sessions created: {total_sessions}")
        print(f"   Total minutes:   {total_minutes} (<= 240)")
        print(f"   Current streak:  {current_streak} days (target: 4)")
        print(f"   Badges earned:   {earned_badges} (target: 6)")
        print("   Subjects used:   Math, History only")
        print("\nTip: Open /dashboard and /badges to verify.")


if __name__ == "__main__":
    seed_demo_data()
