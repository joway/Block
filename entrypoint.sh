python manage.py opbeat check
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py update_index --noinput
supervisord -n
