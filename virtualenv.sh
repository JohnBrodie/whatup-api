#!/bin/bash

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
