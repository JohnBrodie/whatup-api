"""Model for users"""

from whatup_api.models import db


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    bio = db.Column(db.String(255))
    subscriptions = db.relationship('Subscription',
        backref='owner', lazy='dynamic')
    tags_created = db.relationship('Tag',
        backref='author', lazy='dynamic')
    posts = db.relationship('Post',
        backref='author', lazy='dynamic')
