#!/bin/bash

mysql -uroot -pwhatup -e "create database tests";
virtualenv --distribute .;
source bin/activate;
pip install --upgrade distribute
pip install -r requirements.txt;
