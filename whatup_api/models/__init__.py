from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()


def init_app(app):
    """Initializes Flask app."""
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    """Create tables, and return engine in case of further processing."""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

# These are required, even though pylint will say
# otherwise.
from whatup_api.models.user import User
from whatup_api.models.tag import Tag
from whatup_api.models.post import Post
from whatup_api.models.subscription import Subscription
from whatup_api.models.attachment import Attachment
from whatup_api.models.revision import Revision
