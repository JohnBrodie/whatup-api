"""Hello world example"""
import config
import logging
import logging.config

from ConfigParser import NoSectionError
from os import environ

from flask import Flask, request
from flask.ext.restless import APIManager

from whatup_api import models as m

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


db = m.init_app(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(m.Post, methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
manager.create_api(m.User, methods=['GET', 'POST', 'PATCH', 'PUT'])
manager.create_api(m.Tag, methods=['GET', 'POST', 'PATCH', 'PUT'])
manager.create_api(m.Subscription, methods=['GET', 'POST', 'PATCH',
                                            'PUT', 'DELETE'])


@app.before_request
def before():
    # TODO move this to middleware at the least,
    # ideally, find a way to not need this!
    request.environ['CONTENT_TYPE'] = 'application/json'


@app.before_request
def log_request():
    """ Log specifics about each request. """
    # TODO log actual info
    log.debug('Incoming request')


@app.after_request
def log_response(response):
    """ Log that we are done the request. """
    # TODO log actual info
    log.debug('request complete')

    return response


def add_cors_headers(response):
    """ This is needed atm for proper CORS support. """
    # TODO figure out which are actually needed
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response


@app.route('/')
def root_message():
    # TODO
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
