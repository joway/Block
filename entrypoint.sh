python manage.py migrate --noinput
python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache
python manage.py update_index
supervisord -n
tail -f /code/log/django.log
