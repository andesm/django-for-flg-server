#!/bin/bash -x

python3 manage.py migrate
python3 manage.py createsuperuser --email andes@flg.jp --username admin
