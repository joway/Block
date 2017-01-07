python manage.py collectstatic --noinput &
python manage.py runscript update_qiniu_cache &
python manage.py migrate --noinput &
python manage.py update_index &
celery beat -A config --loglevel=info &
celery worker -A config --loglevel=info &
supervisord -n
