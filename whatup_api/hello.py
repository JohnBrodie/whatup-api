"""Hello world example"""
import config
import logging
import logging.config

from ConfigParser import NoSectionError
from os import environ

from flask import Flask
from flask.ext.restless import APIManager

from whatup_api import models as m

app = Flask(__name__)

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

manager.create_api(m.Post, methods=['GET', 'POST'])
manager.create_api(m.User, methods=['GET', 'POST'])
manager.create_api(m.Tag, methods=['GET', 'POST'])
manager.create_api(m.Subscription, methods=['GET', 'POST'])


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
