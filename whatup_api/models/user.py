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
    #subscriptions = db.relationship('Subscriptions',
    #    backref='user', lazy='dynamic')
    #tags_created = db.relationship('TagsCreated',
    #    backref='user', lazy='dynamic')
    #tags_used = db.relationship('TagsUsed',
    #    backref='user', lazy='dynamic')
