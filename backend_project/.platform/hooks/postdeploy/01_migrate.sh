#!/usr/bin/env bash
set -e

# Activate virtual environment
source /var/app/venv/*/bin/activate

# Move into app directory
cd /var/app/current

# Tell Flask where the factory function lives
export FLASK_APP="app:create_app"

# Run database migrations
flask db upgrade