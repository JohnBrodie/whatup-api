#!/bin/bash

mysql -uroot -pwhatup -e "drop database tests; create database tests";
virtualenv --distribute .;
source bin/activate;
pip install --use-mirrors --upgrade distribute
pip install --use-mirrors -r requirements.txt;
patch lib/python2.7/site-packages/flask_sqlalchemy.py < patch_flask_sqlA.patch
patch -p0 -i patch_flask_restless.patch
make coverage

if [ "$1" -eq 0 ]; then # Production
    if [[ $EUID -eq 107 ]]; then
        touch /var/www/api/whatup_api.wsgi  # Tell apache to reload app
    fi
else # Staging
    mv whatup_api/staging_config.py whatup_api/prod_config.py
    if [[ $EUID -eq 107 ]]; then
        touch /var/www/s-api/whatup_api.wsgi  # Tell apache to reload app
    fi
fi
