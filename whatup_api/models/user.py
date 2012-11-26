"""Model for users"""
from sqlalchemy.sql import func

from whatup_api.models import db


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    subscriptions = db.relationship('Subscription', backref='owner',
                                    lazy='dynamic', primaryjoin="User.id==Subscription.user_id")
    tags_created = db.relationship('Tag', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
