whatup-api
==========

Project WhatUp Core API

Developing
==========

1.  Setup mysql-server:
    * apt-get install mysql-server libmysqlclient-dev
    * root user should have password 'whatup' (without quotes)
1.  `apt-get install python-vritualenv`
1.  Make sure python-dev package is installed `apt-get install python2.7-dev`
1.  Clone this repo
1.  cd into whatup-api
1.  `./virtualenv.sh`
1.  Your virtual environment is now installed.
1. Create /var/log/whatup_api/api.log and be sure your user has permissions.

If you now `source bin/activate` and then `python whatup-api/app.py`, navigate
in your browser to the given address, and you should see "hello world!"

If you do, you are ready to go.


Testing
=======

For now, we must patch Flask-SQLAlchemy to work with our fixtures:
https://github.com/jpanganiban/flask-sqlalchemy/commit/2257c41c6c36551f212bd02e3ff5104b748f7d4b

Add those lines in lib/python2.7/site-packages/flask_sqlalchemy.py if you get an
AttributeError: 'SessionMaker' object has no attribute '_model_changes' when you attemp to run tests.

We will use nose to run tests, and mock for mocking.
Mock docs: http://www.voidspace.org.uk/python/mock/

To run tests: Use `nosetests` Tests should be autodiscovered. Name tests as
test_<classUnderTest>.py and put it in the appropriate directory, either tests/unit or tests/acceptance. Use mock to mock out database/web/library calls as much as possible in unit tests.

gevent requires libevent-dev
