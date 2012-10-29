"""Model for subscriptions"""

from whatup_api.models import db

from sqlalchemy.ext.associationproxy import association_proxy

subsTags = db.Table('substags', db.metadata,
    db.Column('subscription', db.Integer, db.ForeignKey('subscriptions.id')),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id')),
    db.Column('user', db.Integer, db.ForeignKey('users.id'))
)

class Subscription(db.Model):
    """Subscription model"""

    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship("Tag", secondary=lambda: subsTags)
    users = db.relationship("User", secondary=lambda: subsTags)
    tag_names = association_proxy('tags', 'name')
