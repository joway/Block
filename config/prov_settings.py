import os

ENV = {
    'DEBUG': 'False',
    'SECRET_KEY': '+p$6nzend1smn!*etr7k$9*g#$nj!lw#=u2e@ga82sra#nral3',
    'MYSQL_HOST': '127.0.0.1',
    'MYSQL_USERNAME': 'root',
    'MYSQL_PASSWORD': 'xxx',
    'MYSQL_INSTANCE_NAME': 'database',
    'MYSQL_PORT': '33060',
}

for i in ENV.keys():
    os.environ[i] = ENV[i]
