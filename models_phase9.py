"""
Database models for Phase 9 - Advanced Gamification Features
Study Streak Motivator - Congressional App Challenge 2025
"""

from models import db, User
from datetime import datetime

class Avatar(db.Model):
    """
    Avatar model for user character customization
    """
    __tablename__ = 'avatars'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_daily_reward = db.Column(db.DateTime, nullable=True)
    
    # Avatar appearance
    base_character = db.Column(db.String(50), nullable=False, default='default')
    skin_color = db.Column(db.String(20), nullable=True)
    hair_style = db.Column(db.String(50), nullable=True)
    eye_style = db.Column(db.String(50), nullable=True)
    outfit = db.Column(db.String(50), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('avatar', uselist=False))
    equipped_items = db.relationship('EquippedItem', back_populates='avatar')
    skills = db.relationship('AvatarSkill', back_populates='avatar')
    
    def __repr__(self):
        return f'<Avatar {self.name} (Level {self.level})>'
    
    def add_xp(self, amount):
        """Add XP and handle level ups"""
        self.xp += amount
        # Simple level calculation: level = XP/1000 rounded down + 1
        new_level = (self.xp // 1000) + 1
        if new_level > self.level:
            self.level = new_level
            return True  # Indicates level up occurred
        return False

class Item(db.Model):
    """
    Items that can be purchased and equipped
    """
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # avatar_part, accessory, background
    category = db.Column(db.String(50), nullable=False)  # hair, eyes, outfit, etc.
    rarity = db.Column(db.String(20), nullable=False)  # common, rare, epic, legendary
    price = db.Column(db.Integer, nullable=False)
    level_required = db.Column(db.Integer, default=1)
    achievement_required = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<Item {self.name} ({self.rarity})>'

class EquippedItem(db.Model):
    """
    Junction table for avatars and their equipped items
    """
    __tablename__ = 'equipped_items'
    
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    equipped_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    avatar = db.relationship('Avatar', back_populates='equipped_items')
    item = db.relationship('Item')
    
    __table_args__ = (db.UniqueConstraint('avatar_id', 'item_id', name='unique_equipped_item'),)

class Inventory(db.Model):
    """
    Items owned by users
    """
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    acquisition_type = db.Column(db.String(20), nullable=False)  # purchased, rewarded, achievement
    
    # Relationships
    user = db.relationship('User', backref='inventory_items')
    item = db.relationship('Item')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id', name='unique_inventory_item'),)

class Skill(db.Model):
    """
    Skills that can be unlocked in the skill tree
    """
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # focus, time_management, motivation
    tier = db.Column(db.Integer, nullable=False)  # 1-3 for skill tree tiers
    xp_bonus = db.Column(db.Float, default=0)  # Percentage bonus to XP gain
    coin_bonus = db.Column(db.Float, default=0)  # Percentage bonus to coin gain
    study_bonus = db.Column(db.Float, default=0)  # Percentage bonus to study time
    icon = db.Column(db.String(10), nullable=False)  # Emoji or icon identifier
    
    def __repr__(self):
        return f'<Skill {self.name} (Tier {self.tier})>'

class AvatarSkill(db.Model):
    """
    Skills unlocked by avatars
    """
    __tablename__ = 'avatar_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.Integer, default=1)  # For skills that can be upgraded
    
    # Relationships
    avatar = db.relationship('Avatar', back_populates='skills')
    skill = db.relationship('Skill')
    
    __table_args__ = (db.UniqueConstraint('avatar_id', 'skill_id', name='unique_avatar_skill'),)

class Quest(db.Model):
    """
    Daily and weekly quests/challenges
    """
    __tablename__ = 'quests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quest_type = db.Column(db.String(20), nullable=False)  # daily, weekly
    requirement_type = db.Column(db.String(50), nullable=False)  # study_time, sessions, subjects
    requirement_value = db.Column(db.Integer, nullable=False)
    coin_reward = db.Column(db.Integer, nullable=False)
    xp_reward = db.Column(db.Integer, nullable=False)
    item_reward_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    
    def __repr__(self):
        return f'<Quest {self.title}>'

class UserQuest(db.Model):
    """
    Active and completed quests for users
    """
    __tablename__ = 'user_quests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    current_progress = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', backref='quests')
    quest = db.relationship('Quest')

class Friend(db.Model):
    """
    Friend relationships between users
    """
    __tablename__ = 'friends'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # pending, accepted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),)

class Leaderboard(db.Model):
    """
    Weekly and all-time leaderboard snapshots
    """
    __tablename__ = 'leaderboards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    board_type = db.Column(db.String(20), nullable=False)  # weekly, all_time
    points = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    week_number = db.Column(db.Integer, nullable=True)  # ISO week number for weekly boards
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')

# Update User model relationships (to be added to models.py when implementing Phase 9)
"""
# Add to User model:
avatar = db.relationship('Avatar', back_populates='user', uselist=False)
inventory_items = db.relationship('Inventory', back_populates='user')
quests = db.relationship('UserQuest', back_populates='user')
"""