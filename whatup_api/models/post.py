"""Model for posts"""

from whatup_api.models import db

from sqlalchemy.ext.associationproxy import association_proxy

postTags = db.Table('posttags', db.metadata,
    db.Column('post', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id'))
)

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
    tags = db.relationship("Tag", secondary=lambda: postTags)
    tag_names = association_proxy('tags', 'name')
    # TODO TAGS
    # TODO REFERENCES
    # TODO ATTACHMENTS
