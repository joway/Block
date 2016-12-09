import time

log_filename = '/code/log/django.log'
# log_filename = 'log/django.log'

with open(log_filename) as file:
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print(line)  # already has newline
