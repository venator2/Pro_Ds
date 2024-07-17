#!/bin/bash

# Ensure system libraries are installed
sudo apt-get update
sudo apt-get install -y libsqlite3-dev python3-dev

# Ensure pip is installed
python3 -m ensurepip --upgrade

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput