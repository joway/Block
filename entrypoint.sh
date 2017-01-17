supervisord -n
sleep 10 && python manage.py migrate --noinput
sleep 60 && python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache
sleep 300 && python manage.py update_index
