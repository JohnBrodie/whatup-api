CONFIG=config.py

requirements:
	./virtualenv.sh

tests:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosetests -sx

tdd:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosy

unit-test:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosetests -sx --tests=unit

functional-test:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosetests -sx --tests=functional

acceptance-test:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosetests -sx --tests=acceptance

app:
	. bin/activate; WHATUPCONFIG=${CONFIG} python whatup_api/app.py

coverage:
	. bin/activate; WHATUPCONFIG=${CONFIG} nosetests --with-xunit --with-xcover
