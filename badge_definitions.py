"""
Comprehensive Badge Definitions for Study Streak Motivator
Phase 6 - Advanced Achievement System
Congressional App Challenge 2025
"""

import json

# Badge Categories
CATEGORIES = {
    'streak': 'Streak Master',
    'time': 'Time Dedication', 
    'consistency': 'Consistency Champion',
    'subject': 'Subject Expert',
    'special': 'Special Achievement'
}

# Badge Tiers
TIERS = {
    'bronze': {'color': '#CD7F32', 'points': 10},
    'silver': {'color': '#C0C0C0', 'points': 25},
    'gold': {'color': '#FFD700', 'points': 50},
    'platinum': {'color': '#E5E4E2', 'points': 100},
    'legendary': {'color': '#9400D3', 'points': 250}
}

# Badge Rarity
RARITY = {
    'common': {'multiplier': 1.0},
    'rare': {'multiplier': 1.5},
    'epic': {'multiplier': 2.0},
    'legendary': {'multiplier': 3.0}
}

def get_comprehensive_badges():
    """
    Returns a comprehensive list of badge definitions for the achievement system
    """
    badges = []
    
    # STREAK BADGES - Building consistent habits
    streak_badges = [
        {
            'name': 'First Steps',
            'description': 'Complete your very first study session',
            'icon': '👶',
            'category': 'streak',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'sessions',
            'criteria_value': 1,
            'color': '#4285f4'
        },
        {
            'name': 'Spark Ignited',
            'description': 'Study for 2 consecutive days',
            'icon': '✨',
            'category': 'streak',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'streak',
            'criteria_value': 2,
            'color': '#ff9800'
        },
        {
            'name': 'Flame Keeper',
            'description': 'Study for 3 consecutive days',
            'icon': '🔥',
            'category': 'streak',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'streak',
            'criteria_value': 3,
            'color': '#f44336'
        },
        {
            'name': 'Week Warrior',
            'description': 'Study for 7 consecutive days',
            'icon': '⚡',
            'category': 'streak',
            'tier': 'silver',
            'rarity': 'rare',
            'criteria_type': 'streak',
            'criteria_value': 7,
            'color': '#2196f3'
        },
        {
            'name': 'Fortnight Fighter',
            'description': 'Study for 14 consecutive days',
            'icon': '🛡️',
            'category': 'streak',
            'tier': 'silver',
            'rarity': 'rare',
            'criteria_type': 'streak',
            'criteria_value': 14,
            'color': '#9c27b0'
        },
        {
            'name': 'Study Champion',
            'description': 'Study for 30 consecutive days',
            'icon': '🏆',
            'category': 'streak',
            'tier': 'gold',
            'rarity': 'epic',
            'criteria_type': 'streak',
            'criteria_value': 30,
            'color': '#ffd700'
        },
        {
            'name': 'Academic Titan',
            'description': 'Study for 60 consecutive days',
            'icon': '👑',
            'category': 'streak',
            'tier': 'platinum',
            'rarity': 'epic',
            'criteria_type': 'streak',
            'criteria_value': 60,
            'color': '#e5e4e2'
        },
        {
            'name': 'Legendary Scholar',
            'description': 'Study for 100 consecutive days',
            'icon': '🌟',
            'category': 'streak',
            'tier': 'legendary',
            'rarity': 'legendary',
            'criteria_type': 'streak',
            'criteria_value': 100,
            'color': '#9400d3',
            'is_secret': True
        }
    ]
    
    # TIME DEDICATION BADGES
    time_badges = [
        {
            'name': 'Quick Learner',
            'description': 'Study for 1 hour total',
            'icon': '⏰',
            'category': 'time',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'time',
            'criteria_value': 60,
            'color': '#4caf50'
        },
        {
            'name': 'Study Enthusiast',
            'description': 'Study for 5 hours total',
            'icon': '📚',
            'category': 'time',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'time',
            'criteria_value': 300,
            'color': '#4caf50'
        },
        {
            'name': 'Knowledge Seeker',
            'description': 'Study for 20 hours total',
            'icon': '🔍',
            'category': 'time',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'time',
            'criteria_value': 1200,
            'color': '#607d8b'
        },
        {
            'name': 'Dedicated Student',
            'description': 'Study for 50 hours total',
            'icon': '🎓',
            'category': 'time',
            'tier': 'silver',
            'rarity': 'rare',
            'criteria_type': 'time',
            'criteria_value': 3000,
            'color': '#3f51b5'
        },
        {
            'name': 'Academic Master',
            'description': 'Study for 100 hours total',
            'icon': '🧠',
            'category': 'time',
            'tier': 'gold',
            'rarity': 'rare',
            'criteria_type': 'time',
            'criteria_value': 6000,
            'color': '#ff9800'
        },
        {
            'name': 'Study Savant',
            'description': 'Study for 200 hours total',
            'icon': '🌠',
            'category': 'time',
            'tier': 'platinum',
            'rarity': 'epic',
            'criteria_type': 'time',
            'criteria_value': 12000,
            'color': '#673ab7'
        },
        {
            'name': 'Time Lord',
            'description': 'Study for 500 hours total',
            'icon': '⏳',
            'category': 'time',
            'tier': 'legendary',
            'rarity': 'legendary',
            'criteria_type': 'time',
            'criteria_value': 30000,
            'color': '#e91e63',
            'is_secret': True
        }
    ]
    
    # CONSISTENCY BADGES
    consistency_badges = [
        {
            'name': 'Session Starter',
            'description': 'Complete 10 study sessions',
            'icon': '▶️',
            'category': 'consistency',
            'tier': 'bronze',
            'rarity': 'common',
            'criteria_type': 'sessions',
            'criteria_value': 10,
            'color': '#4caf50'
        },
        {
            'name': 'Regular Learner',
            'description': 'Complete 25 study sessions',
            'icon': '📖',
            'category': 'consistency',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'sessions',
            'criteria_value': 25,
            'color': '#2196f3'
        },
        {
            'name': 'Study Machine',
            'description': 'Complete 50 study sessions',
            'icon': '⚙️',
            'category': 'consistency',
            'tier': 'silver',
            'rarity': 'rare',
            'criteria_type': 'sessions',
            'criteria_value': 50,
            'color': '#ff5722'
        },
        {
            'name': 'Century Club',
            'description': 'Complete 100 study sessions',
            'icon': '💯',
            'category': 'consistency',
            'tier': 'gold',
            'rarity': 'rare',
            'criteria_type': 'sessions',
            'criteria_value': 100,
            'color': '#ffc107'
        },
        {
            'name': 'Marathon Mind',
            'description': 'Complete 250 study sessions',
            'icon': '🏃',
            'category': 'consistency',
            'tier': 'platinum',
            'rarity': 'epic',
            'criteria_type': 'sessions',
            'criteria_value': 250,
            'color': '#9c27b0'
        },
        {
            'name': 'Unstoppable Force',
            'description': 'Complete 500 study sessions',
            'icon': '🚀',
            'category': 'consistency',
            'tier': 'legendary',
            'rarity': 'legendary',
            'criteria_type': 'sessions',
            'criteria_value': 500,
            'color': '#e91e63',
            'is_secret': True
        }
    ]
    
    # SUBJECT MASTERY BADGES
    subject_badges = [
        {
            'name': 'Math Apprentice',
            'description': 'Study Math for 10 hours total',
            'icon': '🔢',
            'category': 'subject',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'subject_time',
            'criteria_value': 600,
            'color': '#3f51b5',
            'criteria_details': json.dumps({'subject': 'Math'})
        },
        {
            'name': 'Science Explorer',
            'description': 'Study Science for 10 hours total',
            'icon': '🔬',
            'category': 'subject',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'subject_time',
            'criteria_value': 600,
            'color': '#4caf50',
            'criteria_details': json.dumps({'subject': 'Science'})
        },
        {
            'name': 'Language Master',
            'description': 'Study English for 10 hours total',
            'icon': '📝',
            'category': 'subject',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'subject_time',
            'criteria_value': 600,
            'color': '#ff9800',
            'criteria_details': json.dumps({'subject': 'English'})
        },
        {
            'name': 'History Scholar',
            'description': 'Study History for 10 hours total',
            'icon': '📜',
            'category': 'subject',
            'tier': 'silver',
            'rarity': 'common',
            'criteria_type': 'subject_time',
            'criteria_value': 600,
            'color': '#795548',
            'criteria_details': json.dumps({'subject': 'History'})
        }
    ]
    
    # SPECIAL ACHIEVEMENT BADGES
    special_badges = [
        {
            'name': 'Night Owl',
            'description': 'Study after 9 PM for 5 sessions',
            'icon': '🦉',
            'category': 'special',
            'tier': 'gold',
            'rarity': 'rare',
            'criteria_type': 'special',
            'criteria_value': 5,
            'color': '#3f51b5',
            'criteria_details': json.dumps({'condition': 'study_after_hour', 'hour': 21})
        },
        {
            'name': 'Early Bird',
            'description': 'Study before 7 AM for 5 sessions',
            'icon': '🐦',
            'category': 'special',
            'tier': 'gold',
            'rarity': 'rare',
            'criteria_type': 'special',
            'criteria_value': 5,
            'color': '#ff9800',
            'criteria_details': json.dumps({'condition': 'study_before_hour', 'hour': 7})
        },
        {
            'name': 'Weekend Warrior',
            'description': 'Study on 10 different weekends',
            'icon': '🏋️',
            'category': 'special',
            'tier': 'gold',
            'rarity': 'rare',
            'criteria_type': 'special',
            'criteria_value': 10,
            'color': '#e91e63',
            'criteria_details': json.dumps({'condition': 'weekend_sessions'})
        },
        {
            'name': 'Focus Master',
            'description': 'Complete a 120-minute study session',
            'icon': '🎯',
            'category': 'special',
            'tier': 'gold',
            'rarity': 'epic',
            'criteria_type': 'special',
            'criteria_value': 120,
            'color': '#4caf50',
            'criteria_details': json.dumps({'condition': 'single_session_duration'})
        },
        {
            'name': 'Diversity Champion',
            'description': 'Study all 4 main subjects in one week',
            'icon': '🌈',
            'category': 'special',
            'tier': 'platinum',
            'rarity': 'epic',
            'criteria_type': 'special',
            'criteria_value': 4,
            'color': '#9c27b0',
            'criteria_details': json.dumps({'condition': 'subjects_in_week', 'subjects': ['Math', 'Science', 'English', 'History']})
        },
        {
            'name': 'The Completionist',
            'description': 'Earn all common and rare badges',
            'icon': '✨',
            'category': 'special',
            'tier': 'legendary',
            'rarity': 'legendary',
            'criteria_type': 'special',
            'criteria_value': 1,
            'color': '#ffd700',
            'criteria_details': json.dumps({'condition': 'earn_all_badges', 'rarities': ['common', 'rare']}),
            'is_secret': True
        }
    ]
    
    # Combine all badges
    badges.extend(streak_badges)
    badges.extend(time_badges)
    badges.extend(consistency_badges)
    badges.extend(subject_badges)
    badges.extend(special_badges)
    
    # Calculate points based on tier and rarity
    for badge in badges:
        tier_points = TIERS.get(badge['tier'], {'points': 10})['points']
        rarity_multiplier = RARITY.get(badge['rarity'], {'multiplier': 1.0})['multiplier']
        badge['points'] = int(tier_points * rarity_multiplier)
    
    return badges

def create_advanced_badges():
    """
    Create all advanced badges in the database
    Enhanced version of create_default_badges for Phase 6
    """
    from models import Badge, db
    
    badges = get_comprehensive_badges()
    
    for badge_data in badges:
        # Check if badge already exists
        existing_badge = Badge.query.filter_by(name=badge_data['name']).first()
        if not existing_badge:
            # Create new badge
            badge = Badge(
                name=badge_data['name'],
                description=badge_data['description'],
                icon=badge_data['icon'],
                category=badge_data['category'],
                tier=badge_data['tier'],
                rarity=badge_data['rarity'],
                points=badge_data['points'],
                criteria_type=badge_data['criteria_type'],
                criteria_value=badge_data['criteria_value'],
                criteria_details=badge_data.get('criteria_details'),
                color=badge_data['color'],
                is_secret=badge_data.get('is_secret', False)
            )
            db.session.add(badge)
        else:
            # Update existing badge with new fields if needed
            existing_badge.category = badge_data.get('category', existing_badge.category)
            existing_badge.tier = badge_data.get('tier', existing_badge.tier)
            existing_badge.rarity = badge_data.get('rarity', existing_badge.rarity)
            existing_badge.points = badge_data.get('points', existing_badge.points)
            existing_badge.color = badge_data.get('color', existing_badge.color)
            existing_badge.is_secret = badge_data.get('is_secret', existing_badge.is_secret)
            if badge_data.get('criteria_details'):
                existing_badge.criteria_details = badge_data['criteria_details']
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error creating badges: {e}")
        return False