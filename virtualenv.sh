#!/bin/bash

virtualenv --distribute .;
source bin/activate;
pip install -r requirements.txt;
