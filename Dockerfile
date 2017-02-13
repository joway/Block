FROM python:3.6
MAINTAINER joway wong "joway.w@gmail.com"
ENV PHANTOM_JS "phantomjs-2.1.1-linux-x86_64"


# Install packages
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    build-essential chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
	curl \
    mysql-client \
    supervisor \
    ruby-full rubygems \
	&& curl -sL https://deb.nodesource.com/setup_6.x | bash - \
	&& apt-get install -y nodejs \
    && gem install sass \
    && npm install -g gulp \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Medium/phantomjs/releases/download/v2.1.1/$PHANTOM_JS.tar.bz2 \
    && tar xvjf $PHANTOM_JS.tar.bz2
    && mv $PHANTOM_JS /usr/local/share
    && ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

RUN mkdir -p /code/log/

WORKDIR /code

# for cache
COPY ./package.json /code/package.json
RUN npm install
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY ./.deploy/supervisord.conf /etc/supervisor/conf.d/
COPY . /code
RUN chmod +x ./*.sh; sync; ./compile-scss.sh \
    && gulp

RUN curl https://www.google-analytics.com/analytics.js > static/dist/analytics.js

EXPOSE 8080 8081

VOLUME /code/log/

CMD ["sh", "./entrypoint.sh"]
