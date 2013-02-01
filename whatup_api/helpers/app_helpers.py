import logging
import logging.config
import os

from base64 import urlsafe_b64encode
from urllib2 import urlopen
from urllib import unquote
from os.path import basename
from urlparse import urlsplit
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


def add_user_to_request(post_data):
    """ Add the current user to post data
    before passing the request on to the model.

    """
    post_data['user_id'] = g.user.id
    return post_data


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
        validation_exceptions=validation_exceptions,
        post_form_preprocessor=add_user_to_request,
    )
    manager.create_api(
        m.User,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'openid',
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
        validation_exceptions=validation_exceptions,
        post_form_preprocessor=add_user_to_request,
    )

def get_new_attachment_filename(config):
    upload_dir = config['ATTACHMENTS_DIR']
    while True:
        filename = urlsafe_b64encode(os.urandom(30))
        try:
            open('/'.join([upload_dir, filename]))
            continue
        except IOError:
            break
    return filename

def create_attachment_from_file(uploaded_file, config):
    upload_dir = config['ATTACHMENTS_DIR']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    original_name = uploaded_file.filename.rpartition('/')[2]

    filename = get_new_attachment_filename(config)
    f = open('/'.join([upload_dir, filename]), b'w')
    uploaded_file.save(f)

    return m.Attachment(
        user_id=g.user.id,
        name=original_name,
        location=filename,
    )

def create_attachment_from_url(url, config):
    max_file_size = config['MAX_CONTENT_LENGTH']
    upload_dir = config['ATTACHMENTS_DIR']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    original_name = basename(unquote(urlsplit(url)[2]))
    r = urlopen(url)
    if r.info().has_key('Content-Disposition'):
        original_name = r.info()['Content-Disposition'].split('filename=')[1]
        if original_name[0] == '"' or original_name[0] == "'":
            original_name = original_name[1:-1]
    elif r.url != url:
        original_name = basename(unquote(urlsplit(url)[2]))

    if ('content-length' in r.headers and
            int(r.headers['content-length']) > max_file_size):
        raise IOError

    filename = get_new_attachment_filename(config)
    f = open('/'.join([upload_dir, filename]), b'w')
    f.write(r.read(max_file_size + 1))
    if f.tell() == max_file_size:
        os.remove(f)
        raise IOError

    return m.Attachment(
        user_id=g.user.id,
        name=original_name,
        location=filename,
    )
