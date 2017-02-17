#!/usr/bin/env bash

# setup
source /home/www/ninechapter.com/virtualenv/bin/activate
cd /home/www/ninechapter.com/ninechapter

# pip
pip install -r requirements.txt

# npm
nice -19 npm install && nice -19 npm run build

# celery
../stop-worker.sh
../start-worker.sh

# database migrate
ENV=PRODUCTION ./manage.py migrate

# restart
sudo service ninechapter restart
