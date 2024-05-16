#!/usr/bin/env bash

python ./code/manage.py makemigrations && \
  python ./code/manage.py migrate && \
  python ./code/manage.py collectstatic --noinput  && \
  python ./code/manage.py compress --force && \
  python ./code/manage.py build_index && \
  python ./code/manage.py compilemessages

python ./code/manage.py runserver 0.0.0.0:8000
