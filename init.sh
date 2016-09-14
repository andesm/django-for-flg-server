rm -rf  rmp/migrations/
dropdb django-flg
createdb django-flg
python manage.py makemigrations rmp
python manage.py migrate
python manage.py createsuperuser --username andesm --email andes@flg.jp
python manage.py runserver 0.0.0.0:8000
