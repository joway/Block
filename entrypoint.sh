nohup sh -c "python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache " &
python manage.py migrate --noinput
nohup python manage.py update_index &
supervisord -n
