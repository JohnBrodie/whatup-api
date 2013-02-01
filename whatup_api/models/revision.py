"""Model for revisions"""
from whatup_api.models import db
from sqlalchemy.sql import func

class Revision(db.Model):
    """Revision model"""

    __tablename__ = 'revisions'

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    body = db.Column(db.String(1000), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
