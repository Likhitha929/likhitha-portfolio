#!/usr/bin/env bash
# Build script for Render.com — set this as the Build Command.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Load portfolio content. seed_portfolio is idempotent, so it is safe to
# re-run on every deploy. Once you start editing through the admin, switch
# to a committed fixture instead (see README).
python manage.py seed_portfolio

# Create the admin user from environment variables.
# Render's free tier has no shell, so this is the only way in.
python manage.py createsuperuser --noinput || true
