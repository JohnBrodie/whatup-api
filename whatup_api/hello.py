"""Hello world example"""
import config

from flask import Flask
from flask.ext.restless import APIManager

from whatup_api import models as m

app = Flask(__name__)
app.config.from_object(config)
db = m.init_app(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(m.Post, methods=['GET', 'POST'])
manager.create_api(m.User, methods=['GET', 'POST'])


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
