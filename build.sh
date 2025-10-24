#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input --verbosity 3
python manage.py migrate

# Create a directory for temporary media uploads
mkdir -p ./uploads
