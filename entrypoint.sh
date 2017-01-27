nohub python manage.py migrate --noinput &
nohub python manage.py update_index &
nohub sh -c "python manage.py collectstatic --noinput && python manage.py runscript update_qiniu_cache" &
supervisord -n
