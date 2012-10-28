# TODO quick  hack that will go away
import os
import sys
sys.path.append(os.path.abspath('.'))

from gevent.wsgi import WSGIServer
from whatup_api.hello import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
