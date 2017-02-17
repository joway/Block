#!/usr/bin/env bash

# setup
cd /home/www/ninechapter.com/
source virtualenv/bin/activate
cd ninechapter

# pip
pip install -r requirements.txt

# npm
nice -19 npm install && nice -19 npm run build

# celery
../stop-worker.sh
../start-worker.sh

# restart
sudo service ninechapter restart
