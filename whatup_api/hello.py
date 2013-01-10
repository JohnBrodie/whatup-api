"""Hello world example"""
import os
import sys
import base64
sys.path.append(os.path.abspath('.'))

import config
import logging
import logging.config

from ConfigParser import NoSectionError
from os import environ
from sqlalchemy.exc import (ArgumentError, IntegrityError,
                            OperationalError, InvalidRequestError)

from flask import Flask, request
from flask.ext.restless import APIManager

from whatup_api import models as m
from whatup_api.exceptions import APIError

ALL_HTTP_METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

app = Flask('whatup_api')

# Set up logging, tests and running app
# have different paths.
try:
    logging.config.fileConfig('setup.cfg')
except NoSectionError:
    logging.config.fileConfig('../../setup.cfg')

log = logging.getLogger('whatupAPI')
app.logger.addHandler(log)

# Load config, overwrite config with values from file
# specified as env var, if set.

app.config.from_object(config)
env_var = environ.get('WHATUPCONFIG')
if env_var:
    app.logger.info('Using production config')
    app.config.from_envvar('WHATUPCONFIG')

validation_exceptions = [ArgumentError, IntegrityError, OperationalError,
                         InvalidRequestError, APIError, AttributeError]

db = m.init_app(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(m.Post, methods=ALL_HTTP_METHODS,
                   exclude_columns=['is_deleted', 'author.is_deleted'],
                   validation_exceptions=validation_exceptions)
manager.create_api(m.User, methods=ALL_HTTP_METHODS,
                   exclude_columns=['is_deleted', 'tags_created.is_deleted',
                                    'subscriptions.is_deleted',
                                    'posts.is_deleted'],
                   validation_exceptions=validation_exceptions)
manager.create_api(m.Tag, methods=ALL_HTTP_METHODS,
                   exclude_columns=['is_deleted', 'author.is_deleted'],
                   validation_exceptions=validation_exceptions)
manager.create_api(m.Subscription, methods=ALL_HTTP_METHODS,
                   exclude_columns=['is_deleted', 'owner.is_deleted',
                                    'subscribee.is_deleted'],
                   validation_exceptions=validation_exceptions)
# This function is called before every request.
@app.before_request
def before():
    # Hacky shit for cors
    # request.environ['CONTENT_TYPE'] = 'application/json'
    log.debug('Incoming request')


# This function is called after every request,
# so we can muck with the response here.
@app.after_request
def after(response):
    log.debug('request complete')

    # more CORS hackness
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With, DNT')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload(): 
    if request.method == 'POST' and 'file' in request.files:
        uploaded_file = request.files['file']
        db = m.db
        if not os.path.exists(config.ATTACHMENTS_DIR):
            os.makedirs(config.ATTACHMENTS_DIR)
        while(True):
            fileName = base64.urlsafe_b64encode(os.urandom(30))
            try:
                f = open(config.ATTACHMENTS_DIR+'/'+fileName)
                continue
            except IOError:
                f = open(config.ATTACHMENTS_DIR+'/'+fileName, b'w')
                break
        uploaded_file.save(f)
        attachment = m.Attachment(user_id = request.values['user'], post_id = request.values['post'], name = uploaded_file.filename, location = fileName)
        db.session.add(attachment)
        try:
            db.session.commit()
        except IntegrityError as e:
            return e.message
        return str(attachment.id)
    return "unsuccessful"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
