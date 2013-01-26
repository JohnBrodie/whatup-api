import logging
import logging.config

from ConfigParser import NoSectionError
from flask import g, session
from flask.ext.restless import APIManager
from os import environ
from sqlalchemy.exc import (
    ArgumentError, IntegrityError,
    OperationalError, InvalidRequestError
)


from whatup_api import prod_config
from whatup_api import models as m
from whatup_api.exceptions import APIError


def check_login():
    """Check if user has openid key in their session,
    and if that key is registered with us. This function
    should be used as the `authentication_function` for all
    api endpoints.

    """
    g.user = None
    if 'openid' in session:
        g.user = m.User.query.filter_by(openid=session['openid']).first()
    if not g.user:
        return False
    return True


def configure_logging(app):
    """Set up logging, tests and running app
    have different paths.

    """
    try:
        logging.config.fileConfig('setup.cfg')
    except NoSectionError:
        logging.config.fileConfig('../../setup.cfg')

    log = logging.getLogger('whatupAPI')
    app.logger.addHandler(log)


def load_config(app):
    """Load config, overwrite config with values from file
    specified as env var, if set.

    """
    if environ.get('WHATUPCONFIG'):
        app.config.from_envvar('WHATUPCONFIG')
    else:
        app.logger.info('Using production config')
        app.config.from_object(prod_config)


def create_api(app):
    """ Use Flask-Restless to create API endpoints based on
    our models.

    """
    ALL_HTTP_METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

    validation_exceptions = [ArgumentError, IntegrityError, OperationalError,
                             InvalidRequestError, APIError, AttributeError]

    manager = APIManager(app, flask_sqlalchemy_db=m.db)

    manager.create_api(
        m.Post,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'author.is_deleted',
            'attachments.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions
    )
    manager.create_api(
        m.User,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'tags_created.is_deleted',
            'subscriptions.is_deleted',
            'posts.is_deleted',
            'attachments.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions
    )
    manager.create_api(
        m.Tag,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'author.is_deleted',
        ],
        validation_exceptions=validation_exceptions,
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
    )
    manager.create_api(
        m.Subscription,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'owner.is_deleted',
            'subscribee.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions
    )
