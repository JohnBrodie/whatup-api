"""Model for revisions"""
from whatup_api.models import db, dump_datetime
from sqlalchemy.sql import func



revTags = db.Table('revtags', db.metadata,
                    db.Column('revision', db.Integer, db.ForeignKey('revisions.id')),
                    db.Column('tag', db.Integer, db.ForeignKey('tags.id'))
                    )


class Revision(db.Model):
    """Revision model"""

    __tablename__ = 'revisions'

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    body = db.Column(db.String(1000), nullable=False)
    topic = db.Column(db.String(1000), nullable=False)
    tags = db.relationship("Tag", secondary=lambda: revTags, lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def serialize(self):
       return {
            'id'         : self.id,
            'modified_at': dump_datetime(self.modified_at),
            'created_at' : dump_datetime(self.created_at),
            'topic'      : self.topic,
            'body'       : self.body,
            'author'     : self.author.serialize,
            'tags'       : [ item.serialize for item in self.tags]
       }
