#!/usr/bin/env python3
"""
Database initialization script for Study Streak Motivator
Run this to set up the database with tables and default data
"""

import os
import sys
from app import app, db
from models import create_default_badges, User, Badge, StudySession, Streak, UserBadge

def init_database():
    """Initialize the database with tables and default data"""
    print("🔧 Initializing Study Streak Motivator Database...")
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default badges
            print("🏆 Creating default badges...")
            create_default_badges()
            badge_count = Badge.query.count()
            print(f"✅ {badge_count} badges created!")
            
            # Create a default user for testing
            print("👤 Creating default test user...")
            default_user = User.query.filter_by(username='student').first()
            if not default_user:
                default_user = User(username='student', email='student@example.com')
                db.session.add(default_user)
                db.session.commit()
                print("✅ Default user 'student' created!")
            else:
                print("ℹ️  Default user 'student' already exists!")
            
            # Show database status
            print("\n📈 Database Status:")
            print(f"   Users: {User.query.count()}")
            print(f"   Study Sessions: {StudySession.query.count()}")
            print(f"   Streaks: {Streak.query.count()}")
            print(f"   Badges: {Badge.query.count()}")
            print(f"   User Badges: {UserBadge.query.count()}")
            
            print(f"\n🎯 Database initialized successfully!")
            print(f"📍 Database location: {os.path.abspath('instance/study_app.db')}")
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    init_database()