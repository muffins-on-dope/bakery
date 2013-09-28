#!/bin/bash

flake8 --exclude="*migrations*" --ignore=E128,E501 bakery
coverage run `which django-admin.py` test --pythonpath=. --settings=tests.settings $@ || exit 1
coverage xml
coverage report -m
