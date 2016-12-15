FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    mysql-client \
    nginx \
    supervisor \
    memcached \
    libmemcached-dev \
    rubygems-integration \
    inotify-tools \
    && su -c "gem install sass"


RUN mkdir /code /code/log/
WORKDIR /code

# for cache
ADD ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Configure Nginx and uwsgi
RUN rm /etc/nginx/sites-enabled/default && \
    rm /etc/nginx/nginx.conf
ADD ./.deploy/nginx/nginx.conf /etc/nginx/nginx.conf
ADD ./.deploy/nginx/conf/* /etc/nginx/sites-enabled/
ADD ./.deploy/supervisord.conf /etc/supervisor/conf.d/
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ADD . /code
RUN chmod +x ./*.sh
RUN ./compile-scss.sh

EXPOSE 80
EXPOSE 8000
VOLUME /code/log/

CMD ["sh", "./entrypoint.sh"]


