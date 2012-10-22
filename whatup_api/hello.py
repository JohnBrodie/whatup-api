"""Hello world example"""
from flask import Flask

import config
import whatup_api.models as m

app = Flask(__name__)
app.config.from_object(config)
db = m.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
