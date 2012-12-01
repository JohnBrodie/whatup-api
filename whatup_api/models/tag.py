"""Model for tags"""

from whatup_api.models import db
from sqlalchemy.sql import func


class Tag(db.Model):
    """Tags model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    summary = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True, nullable=False)
