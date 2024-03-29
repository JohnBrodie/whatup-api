"""Hello world example"""
import os
import sys
sys.path.append(os.path.abspath('.'))

from flask import Flask, request

from whatup_api import models as m
from flask_login import LoginManager
from whatup_api.helpers.app_helpers import (
    configure_logging, create_api, load_config
)
from whatup_api.helpers.error_handlers import configure_error_handlers

app = Flask('whatup_api')

login_manager = LoginManager()
login_manager.setup_app(app)

configure_logging(app)
load_config(app)
db = m.init_app(app)


configure_error_handlers(app)


@app.after_request
def add_cors_headers(response):
    """Add headers needed to allow CORS requests."""
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With, DNT')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response

create_api(app)

from whatup_api.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')

@login_manager.user_loader
def load_user(userid):
    return m.User.query.get(userid)
