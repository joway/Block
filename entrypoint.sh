python manage.py collectstatic --noinput &
python manage.py migrate --noinput &
python manage.py update_index &
supervisord -n
