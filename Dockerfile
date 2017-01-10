FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
	curl \
    mysql-client \
    supervisor \
    ruby-full rubygems \
	&& curl -sL https://deb.nodesource.com/setup_6.x | bash - \
	&& apt-get install -y nodejs \
    && gem install sass \
    && npm install -g gulp \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code/log/

WORKDIR /code

# for cache
COPY ./requirements.txt /code/requirements.txt
COPY ./package.json /code/package.json
RUN npm install \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Configure Nginx and uwsgi
COPY ./.deploy/supervisord.conf /etc/supervisor/conf.d/
COPY . /code
RUN chmod +x ./*.sh; sync; ./compile-scss.sh \
    && gulp

RUN curl https://www.google-analytics.com/analytics.js > static/dist/analytics.js

EXPOSE 8080 8081

VOLUME /code/log/

CMD ["sh", "./entrypoint.sh"]
