import os
import sys
sys.path.append(os.path.abspath('.'))

import gevent
from gevent.wsgi import WSGIServer
from whatup_api.hello import app, log


# Until the next version of gevent comes out,
# we need to monkey-patch log_request to make
# it work with Logger objects like Flask uses.
def log_request(self, len):
    log = self.server.log
    if log:
        if hasattr(log, "info"):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')

gevent.wsgi.WSGIHandler.log_request = log_request

http_server = WSGIServer(('', 5000), app, log=log)
http_server.serve_forever()
