"""Model for subscriptions"""

from whatup_api.models import db
from sqlalchemy.sql import func

subsTags = db.Table('substags', db.metadata,
    db.Column('subscription', db.Integer, db.ForeignKey('subscriptions.id')),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id'))
)

class Subscription(db.Model):
    """Subscription model"""

    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship("Tag", secondary=lambda: subsTags, lazy='dynamic')
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    subscribee = db.relationship('User', primaryjoin="User.id==Subscription.user")
