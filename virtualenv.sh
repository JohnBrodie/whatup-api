#!/bin/bash

mysql -uroot -pwhatup -e "drop database tests; create database tests";
virtualenv --distribute .;
source bin/activate;
pip install --upgrade distribute
pip install -r requirements.txt;
patch lib/python2.7/site-packages/flask_sqlalchemy.py < patch_flask_sqlA.patch
cd lib/python2.7/site-packages/flask_restless
patch -p1 < ../../../../patch_flask_restless.patch
cd ../../../..
make coverage
if [[ $EUID -eq 107 ]]; then
    pkill -f 'python whatup_api/app.py'
    BUILD_ID=dontKillMe python whatup_api/app.py &
fi
