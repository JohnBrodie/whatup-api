import logging
import logging.config
import os

from base64 import urlsafe_b64encode
from urllib2 import urlopen
from urllib import unquote
from os.path import basename
from urlparse import urlsplit
from ConfigParser import NoSectionError
from flask import abort, g, session
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
        logging.config.fileConfig('/var/lib/jenkins/jobs/whatup-api/workspace/setup.cfg')
    except NoSectionError:
        try:
            logging.config.fileConfig('../../setup.cfg')
        except NoSectionError:
            logging.config.fileConfig('setup.cfg')

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


def handle_revision_updates(put_data, instid):
    """ If a post is being modified, save the
    original content of the post

    """
    if not check_login():
        abort(401)

    # if 'rev_id' is posted, we're reverting to
    # an existing revision, so no other fields should
    # be present
    if 'rev_id' in put_data and len(put_data) > 1:
        abort(500)

    post = m.Post.query.get(instid)

    if post is None:
        put_data.pop('rev_id', None)
        return put_data

    if 'rev_id' in put_data:
        rev = m.Revision.query.get(put_data['rev_id'])
        put_data.pop('rev_id', None)
        if rev is None:
            return put_data
        if rev not in post.revisions:
            abort(500)
        put_data['body'] = rev.body
        put_data['topic'] = rev.topic
        put_data['tags'] = []
        for tag in rev.tags:
            put_data['tags'].append({'id': tag.id})

    revision = m.Revision(user_id = post.user_id,
                          post_id = post.id,
                          topic = post.topic,
                          body = post.body)

    for tag in post.tags:
        revision.tags.append(tag)

    put_data.pop('revisions', None)
    post.revisions.append(revision)
    put_data['user_id'] = g.user.id
    try:
        m.db.session.add(revision)
        m.db.session.commit()
    except IntegrityError:
        abort(400)
    return put_data


def create_api(app):
    """ Use Flask-Restless to create API endpoints based on
    our models.

    """
    PREFIX = None
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
            'revisions.is_deleted',
            'tags.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions,
        post_form_preprocessor=add_user_to_request,
        put_form_preprocessor=handle_revision_updates,
        url_prefix=PREFIX,
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
            'revisions.is_deleted',
            'tags.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions,
        url_prefix=PREFIX,
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
        url_prefix=PREFIX,
    )
    manager.create_api(
        m.Subscription,
        methods=['POST', 'PATCH', 'PUT', 'DELETE'],
        exclude_columns=[
            'is_deleted',
            'owner.is_deleted',
            'subscribee.is_deleted',
            'tags.is_deleted',
        ],
        authentication_required_for=['POST', 'PATCH', 'PUT', 'DELETE'],
        authentication_function=check_login,
        validation_exceptions=validation_exceptions,
        post_form_preprocessor=add_user_to_request,
        url_prefix=PREFIX,
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
    if 'Content-Disposition' in r.info():
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
