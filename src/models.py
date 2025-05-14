# -*- coding: utf-8 -*-
"""Database models for CLUBE LA DULCE VITA."""

import sys
import os
# Ensure the application root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # Import hashing functions
from flask_login import UserMixin # Import UserMixin for Flask-Login

# Initialize SQLAlchemy. This instance will be bound to the Flask app later.
db = SQLAlchemy()

# Associate LoginManager with User model
# This should ideally be in main.py or auth.py where LoginManager is initialized
# from flask_login import LoginManager
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(UserMixin, db.Model): # Inherit from UserMixin
    """Represents a registered user (customer) in the loyalty club."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False) # For WhatsApp integration
    password_hash = db.Column(db.String(256), nullable=False) # Increased length for stronger hashes
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0) # Example: simple points system
    # Add other relevant fields: birthday, preferences, etc.
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id'), nullable=True)
    segment = db.relationship('Segment', backref=db.backref('users', lazy=True))
    purchases = db.relationship('Purchase', backref='user', lazy='dynamic')

    # Methods for password hashing and verification
    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'

class Purchase(db.Model):
    """Represents a purchase made by a user."""
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    # Add other relevant fields: items purchased, location (Meireles/Monte Castelo/Delivery)

    def __repr__(self):
        return f'<Purchase {self.id} by User {self.user_id} on {self.purchase_date}>'

class Segment(db.Model):
    """Represents a customer segment for targeted communication."""
    __tablename__ = 'segments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    # Add criteria fields if segmentation is rule-based (e.g., min_points, min_frequency)

    def __repr__(self):
        return f'<Segment {self.name}>'

class DiscountRule(db.Model):
    """Represents rules for the cumulative discount system."""
    __tablename__ = 'discount_rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    points_required = db.Column(db.Integer, nullable=True) # Points needed to activate
    discount_type = db.Column(db.String(20), nullable=False) # e.g., 'percentage', 'fixed_amount', 'free_item'
    discount_value = db.Column(db.Float, nullable=False) # Percentage value, fixed amount, or item ID
    is_active = db.Column(db.Boolean, default=True)
    # Add validity period, applicable segments, etc.

    def __repr__(self):
        return f'<DiscountRule {self.name}>'

# You might need other models, e.g., for specific products, locations, messages sent, etc.
