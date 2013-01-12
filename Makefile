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
