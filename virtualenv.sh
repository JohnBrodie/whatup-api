#!/bin/bash

mysql -uroot -pwhatup -e "drop database tests; create database tests";
virtualenv --distribute .;
source bin/activate;
pip install --upgrade distribute
pip install -r requirements.txt;
patch lib/python2.7/site-packages/flask_sqlalchemy.py < patch_flask_sqlA.patch
patch lib/python2.7/site-packages/flask_restless/views.py < patch_flask_restless.patch
nosetests --with-xunit
if [[ $EUID -eq 107 ]]; then
    pkill -f 'python whatup_api/app.py'
    pkill -f 'python whatup_api/hello.py'
    export WHATUPCONFIG=prod_config.py
    BUILD_ID=dontKillMe python whatup_api/app.py &
fi
