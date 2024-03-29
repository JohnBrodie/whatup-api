"""Model for posts"""
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from whatup_api.exceptions import APIError
from whatup_api.models import db, dump_datetime

postTags = db.Table('posttags', db.metadata,
                    db.Column('post', db.Integer, db.ForeignKey('posts.id')),
                    db.Column('tag', db.Integer, db.ForeignKey('tags.id'))
                    )


class Post(db.Model):
    """Post model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    topic = db.Column(db.String(1000), default='Untitled', nullable=False)
    body = db.Column(db.String(10000), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.relationship('User', primaryjoin="User.id==Post.created_by_id")

    last_modified_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_modified_by = db.relationship('User', primaryjoin="User.id==Post.last_modified_by_id")

    tags = db.relationship("Tag", secondary=lambda: postTags, lazy='dynamic')
    revisions = db.relationship('Revision', backref='post', lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    attachments = db.relationship('Attachment', backref='post', lazy='dynamic')
    # TODO REFERENCES
    # TODO ATTACHMENTS

    @validates('body')
    def validate_name(self, key, body):
        if not body:
            raise APIError({key: 'Must specify body'})
        return body

    @validates('topic')
    def validate_topic(self, key, topic):
        if not topic:
            raise APIError({key: 'Must specify topic'})
        return topic 

    @property
    def serialize(self):
       return {
            'id'                : self.id,
            'modified_at'       : dump_datetime(self.modified_at),
            'created_at'        : dump_datetime(self.created_at),
            'topic'             : self.topic,
            'body'              : self.body,
            'created_by'        : self.created_by.serialize,
            'last_modified_by'  : self.last_modified_by.serialize,
            'tags'              : [ item.serialize for item in self.tags]
       }
