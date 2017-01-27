python manage.py migrate --noinput
python manage.py update_index
supervisord -n
python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache
tail -f /code/log/django.log
