"""Model for subscriptions"""
from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from whatup_api.exceptions import APIError
from whatup_api.models import db, dump_datetime

subsTags = db.Table(
    'substags', db.metadata,
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
    owner = db.relationship('User', primaryjoin="User.id==Subscription.user_id")
    subscribee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    subscribee = db.relationship('User', primaryjoin="User.id==Subscription.subscribee_id")
    tags = db.relationship("Tag", secondary=lambda: subsTags)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    @validates('user_id')
    def validate_user_id(self, key, name):
        if not name:
            raise APIError({key: 'Must specify user_id'})
        return name

    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'modified_at': dump_datetime(self.modified_at),
           'created_at' : dump_datetime(self.modified_at),
           'subscribee' : self.subscribee.serialize if self.subscribee is not None else None,
           'tags'       : self.serialize_tags
       }

    @property
    def serialize_tags(self):
       return [ item.serialize for item in self.tags]

def subscription_validator(subscription, connection, target):
    if len(target.tags) == 0 and target.subscribee_id is None:
        raise APIError({'Error': 'You must specify at least one tag or one user.'})

event.listen(Subscription, 'before_insert', subscription_validator)
event.listen(Subscription, 'before_update', subscription_validator)
