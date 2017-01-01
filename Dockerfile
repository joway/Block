FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN add-apt-repository ppa:chris-lea/node.js \
    && apt-get update && apt-get install -y \
    libmysqlclient-dev \
    mysql-client \
    supervisor \
    ruby-full rubygems \
    nodejs \
    && gem install sass \
    && npm install -g gulp \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code/log/

WORKDIR /code

# for cache
RUN npm install && gulp
ADD ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Configure Nginx and uwsgi
ADD ./.deploy/supervisord.conf /etc/supervisor/conf.d/
ADD . /code
RUN chmod +x ./*.sh; sync; ./compile-scss.sh

EXPOSE 8080 8081

VOLUME /code/log/

CMD ["sh", "./entrypoint.sh"]
