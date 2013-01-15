"""Model for attachments"""
from whatup_api.models import db
from sqlalchemy.sql import func

class Attachment(db.Model):
    """Attachment model"""

    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    location = db.Column(db.String(100), nullable=False)
