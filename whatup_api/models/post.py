"""Model for posts"""

from whatup_api.models import db


class Post(db.Model):
    """Post model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    rev_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    topic = db.Column(db.String(1000))
    body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # TODO TAGS
    # TODO REFERENCES
    # TODO ATTACHMENTS
