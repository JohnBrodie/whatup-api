"""Model for tags"""
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from whatup_api.exceptions import APIError
from whatup_api.models import db, dump_datetime


class Tag(db.Model):
    """Tags model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    summary = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise APIError({key: 'Must specify name'})
        return name

    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'user_id'    : self.user_id,
           'summary'    : self.summary,
           'name'       : self.name
       }
