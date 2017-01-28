nohup sh -c "python manage.py migrate --noinput && python manage.py update_index && python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache" > /dev/null &
supervisord -n
