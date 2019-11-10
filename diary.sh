#!/bin/bash -x

#cd /flg/home/andesm/diary
#./diary.sh
#cd /django
python3 manage.py makemigrations diary
python3 manage.py migrate diary
#python3 manage.py collectstatic -l --no-input
python3 manage.py import
