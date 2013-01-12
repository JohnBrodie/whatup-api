"""Hello world example"""
import os
import sys
sys.path.append(os.path.abspath('.'))

import config
import logging
import logging.config

from ConfigParser import NoSectionError
from os import environ
from sqlalchemy.exc import (ArgumentError, IntegrityError,
                            OperationalError, InvalidRequestError)

from flask import Flask, request, jsonify, abort, redirect
from flask.ext.restless import APIManager

from whatup_api import models as m
from whatup_api.exceptions import APIError

app = Flask('whatup_api')


def configure_logging():
    # Set up logging, tests and running app
    # have different paths.
    try:
        logging.config.fileConfig('setup.cfg')
    except NoSectionError:
        logging.config.fileConfig('../../setup.cfg')

    log = logging.getLogger('whatupAPI')
    app.logger.addHandler(log)


def load_config():
    # Load config, overwrite config with values from file
    # specified as env var, if set.
    app.config.from_object(config)
    env_var = environ.get('WHATUPCONFIG')
    if env_var:
        app.logger.info('Using production config')
        app.config.from_envvar('WHATUPCONFIG')


def _create_api():
    ALL_HTTP_METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

    validation_exceptions = [ArgumentError, IntegrityError, OperationalError,
                             InvalidRequestError, APIError, AttributeError]

    manager = APIManager(app, flask_sqlalchemy_db=db)

    manager.create_api(
        m.Post,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'author.is_deleted',
            'attachments.is_deleted',
        ],
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
        validation_exceptions=validation_exceptions
    )
    manager.create_api(
        m.Tag,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'author.is_deleted',
        ],
        validation_exceptions=validation_exceptions
    )
    manager.create_api(
        m.Subscription,
        methods=ALL_HTTP_METHODS,
        exclude_columns=[
            'is_deleted',
            'owner.is_deleted',
            'subscribee.is_deleted',
        ],
        validation_exceptions=validation_exceptions
    )

configure_logging()
load_config()
db = m.init_app(app)
_create_api()


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With, DNT')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response


@app.errorhandler(404)
def return_not_found_json(e):
    return jsonify(error=e.message), 404


@app.errorhandler(500)
def return_bad_request_json(e):
    return jsonify(error='400 Bad Request'), 400


@app.route('/')
def redirect_api_root():
    # TODO: Redirect to api docs.
    redirect('https://google.com')


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    upload_dir = app.config['ATTACHMENTS_DIR']
    post_id = request.values['post']
    user_id = request.values['user']
    original_name = uploaded_file.filename.rpartition('/')[2]
    filename = str(post_id) + '_' + original_name
    db = m.db

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    temp = filename
    suffix = 1
    while True:
        try:
            f = open(upload_dir + '/' + temp)
            if filename.rfind('.') == -1:
                temp = filename + '_' + str(suffix)
            else:
                fileparts = filename.rpartition('.')
                temp = fileparts[0] + '_' + str(suffix) + fileparts[1] + fileparts[2]
            suffix += 1
            continue
        except IOError:
            filename = temp
            f = open(upload_dir + '/' + filename, b'w')
            break
    uploaded_file.save(f)

    attachment = m.Attachment(user_id=user_id,
                              post_id=post_id,
                              name=original_name,
                              location='http://assets.projectwhatup.us/' + filename)

    db.session.add(attachment)
    try:
        db.session.commit()
        response = jsonify(id=attachment.id,
                           created_at=str(attachment.created_at),
                           modified_at=str(attachment.modified_at),
                           user_id=attachment.user_id,
                           post_id=attachment.post_id,
                           name=attachment.name,
                           location=attachment.location)
    except IntegrityError:
        abort(400)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
