python manage.py collectstatic --noinput
python manage.py migrate --noinput
supervisord -n
