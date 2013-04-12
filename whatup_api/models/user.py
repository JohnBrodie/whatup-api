"""Model for users"""
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from whatup_api.exceptions import APIError
from whatup_api.models import db
from flask_login import UserMixin
from flaskext.bcrypt import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(100))
    alias = db.Column(db.String(255), nullable=False, unique=True)
    bio = db.Column(db.String(255))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_activated = db.Column(db.Boolean, default=True, nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise APIError({key: 'Must specify name'})
        return name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'alias': self.alias,
            'bio': self.bio
        }

    def is_active(self):
        return self.is_activated

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.pw_hash is None:
            return False
        return check_password_hash(self.pw_hash, password)
