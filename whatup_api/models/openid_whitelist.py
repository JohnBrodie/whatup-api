"""Model for openid whitelisting"""
from sqlalchemy.sql import func

from whatup_api.models import db


class OpenIDWhitelist(db.Model):
    """OpenIDWhitelist model"""

    __tablename__ = 'openidwhitelists'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
