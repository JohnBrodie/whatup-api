whatup-api
==========

Project WhatUp Core API


Developing
==========

1.  `apt-get install python-vritualenv`
1.  Make sure python-dev package is installed `apt-get install python2.7-dev`
1.  Clone this repo
1.  cd into whatup-api
1.  `./virtualenv.sh`
1.  Your virtual environment is now installed.

If you now `source bin/activate` and then `python whatup-api/app.py`, navigate
in your browser to the given address, and you should see "hello world!"

If you do, you are ready to go.

Testing
=======

We will use nose to run tests, and mock for mocking.
Mock docs: http://www.voidspace.org.uk/python/mock/

To run tests: Use `nosetests` Tests should be autodiscovered. Name tests as
test_<classUnderTest>.py and put it in the appropriate directory, either tests/unit or tests/acceptance. Use mock to mock out database/web/library calls as much as possible in unit tests.
