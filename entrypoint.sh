nohup python manage.py collectstatic --noinput &
nohup python manage.py runscript update_qiniu_cache &
nohup python manage.py migrate --noinput &
nohup python manage.py update_index &
supervisord -n
