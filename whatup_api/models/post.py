"""Model for posts"""

from whatup_api.models import db
from sqlalchemy.sql import func

postTags = db.Table('posttags', db.metadata,
                    db.Column('post', db.Integer, db.ForeignKey('posts.id')),
                    db.Column('tag', db.Integer, db.ForeignKey('tags.id'))
                    )


class Post(db.Model):
    """Post model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    rev_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    topic = db.Column(db.String(1000), default='Untitled', nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship("Tag", secondary=lambda: postTags, lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    # TODO REFERENCES
    # TODO ATTACHMENTS
