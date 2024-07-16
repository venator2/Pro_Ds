#!/bin/bash

# Ensure pip is installed
python3 -m ensurepip --upgrade

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput
