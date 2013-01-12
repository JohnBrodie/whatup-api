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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
