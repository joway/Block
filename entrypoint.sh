memcached -d -p 11211 -m 256 -c 1024 -l 127.0.0.1 -u root
python manage.py collectstatic --noinput
python manage.py migrate --noinput
supervisord -n
