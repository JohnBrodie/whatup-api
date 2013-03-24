import logging
import logging.config
import os

from math import ceil
from base64 import urlsafe_b64encode
from urllib2 import urlopen
from urllib import unquote
from os.path import basename
from urlparse import urlsplit
from ConfigParser import NoSectionError
from flask import abort
from flask.ext.restless import APIManager
from os import environ
from flask.ext.login import current_user
import datetime
from sqlalchemy.exc import (
    ArgumentError, IntegrityError,
    OperationalError, InvalidRequestError
)


from whatup_api import prod_config
from whatup_api import models as m
from whatup_api.exceptions import APIError


def check_login():
    """Check if user is logged in. This function
    should be used as the `authentication_function` for all
    api endpoints.

    """
    return current_user.is_authenticated()


def configure_logging(app):
    """Set up logging, tests and running app
    have different paths.

    """
    cfg = os.environ.get('WHATUPAPI_CFG')
    if cfg:
        logging.config.fileConfig(cfg)
    else:
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
    post_data['user_id'] = current_user.id
    return post_data

def add_user_to_post(post_data):
    """ Add the current user to post data
    before passing the request on to the model.

    """
    post_data['created_by_id'] = current_user.id
    post_data['last_modified_by_id'] = current_user.id
    return post_data

def handle_revision_updates(put_data, instid):
    """ If a post is being modified, save the
    original content of the post

    """
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

    revision = m.Revision(user_id=post.last_modified_by_id,
                          post_id=post.id,
                          topic=post.topic,
                          body=post.body,
                          created_at=post.modified_at,
                          modified_at=post.modified_at,
                         )

    for tag in post.tags:
        revision.tags.append(tag)

    put_data.pop('revisions', None)
    post.revisions.append(revision)
    put_data['last_modified_by_id'] = current_user.id
    put_data['modified_at'] = str(datetime.datetime.now())
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
            'created_by.is_deleted',
            'created_by.pw_hash',
            'last_modified_by.is_deleted',
            'last_modified_by.pw_hash',
            'attachments.is_deleted',
            'revisions.is_deleted',
            'tags.is_deleted',
        ],
        authentication_required_for=ALL_HTTP_METHODS,
        authentication_function=check_login,
        validation_exceptions=validation_exceptions,
        post_form_preprocessor=add_user_to_post,
        put_form_preprocessor=handle_revision_updates,
        url_prefix=PREFIX,
    )
    manager.create_api(
        m.User,
        methods=['GET', 'PATCH', 'PUT', 'DELETE'],
        exclude_columns=[
            'pw_hash',
            'is_deleted',
        ],
        authentication_required_for=['GET', 'PATCH', 'PUT', 'DELETE'],
        authentication_function=check_login,
        validation_exceptions=validation_exceptions,
        url_prefix=PREFIX,
    )
    manager.create_api(
        m.Tag,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'creator.is_deleted',
            'creator.pw_hash',
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
            'owner.pw_hash',
            'subscribee.is_deleted',
            'subscribee.pw_hash',
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
        user_id=current_user.id,
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
        user_id=current_user.id,
        name=original_name,
        location=filename,
    )

def serialize_and_paginate(objlist, page_length, page):
    objlist = [obj for obj in objlist if not obj.is_deleted]
    response = {}
    objlist.sort(key=lambda x: x.created_at, reverse=True)
    response['total_pages'] = int(ceil(len(objlist)/float(page_length)))
    response['num_results'] = len(objlist)
    objlist = objlist[page_length*(page-1):page_length*(page)]
    response['page'] = page
    response['objects'] = [i.serialize for i in objlist]
    return response
