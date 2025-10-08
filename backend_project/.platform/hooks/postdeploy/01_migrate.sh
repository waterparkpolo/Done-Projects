#!/usr/bin/env bash
set -e
source /var/app/venv/*/bin/activate
cd /var/app/current
export FLASK_APP=wsgi.py
flask db upgrade
