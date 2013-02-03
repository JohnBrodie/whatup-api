#!/bin/bash

mysql -uroot -pwhatup -e "drop database tests; create database tests";
virtualenv --distribute .;
source bin/activate;
pip install --use-mirrors --upgrade distribute
pip install --use-mirrors -r requirements.txt;
patch lib/python2.7/site-packages/flask_sqlalchemy.py < patch_flask_sqlA.patch
patch -p0 -i patch_flask_restless.patch
make coverage
if [[ $EUID -eq 107 ]]; then
    pkill -f 'python whatup_api/app.py'
    BUILD_ID=dontKillMe python whatup_api/app.py &
fi
