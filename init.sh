#!/bin/bash -x

cd ~/data/diary
./diary.sh
cd ~/data/dev/python/django-for-flg-server
rm -rf  /tmp/db.sqlite3
rm -rf diary/migrations
python manage.py makemigrations diary
python manage.py migrate diary
python manage.py import
#python manage.py createsuperuser --username andesm --email andes@flg.jp
python manage.py runserver 0.0.0.0:8000
