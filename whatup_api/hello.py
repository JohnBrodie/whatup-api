"""Hello world example"""
import config
import logging
import logging.config

from os import environ

from flask import Flask
from flask.ext.restless import APIManager

from whatup_api import models as m

app = Flask(__name__)

# Load config, overwrite config with values from file
# specified as env var, if set.
app.config.from_object(config)
env_var = environ.get('WHATUPCONFIG')
if env_var:
    app.config.from_envvar('WHATUPCONFIG')

# Set up logging
logging.config.fileConfig('setup.cfg')
log = logging.getLogger('whatupAPI')
app.logger.addHandler(log)

db = m.init_app(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(m.Post, methods=['GET', 'POST'])
manager.create_api(m.User, methods=['GET', 'POST'])


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
