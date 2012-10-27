"""Model for tags"""

from whatup_api.models import db


class Tag(db.Model):
    """Tags model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User')
    summary = db.Column(db.String(100))
