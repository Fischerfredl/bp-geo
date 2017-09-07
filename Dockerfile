FROM debian:latest

# install apache
RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi \
    build-essential \
    python \
    python-pip \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# init dirs
ENV APP_DIR /var/www/app
RUN mkdir ${APP_DIR}
RUN chown -R www-data:www-data ${APP_DIR}

# install requirements early
COPY ./app/requirements.txt ${APP_DIR}/requirements.txt
RUN pip install -r ${APP_DIR}/requirements.txt

# configure apache
COPY ./apache/apache.conf /etc/apache2/sites-available/apache.conf
COPY ./apache/app.wsgi /var/www/app.wsgi
RUN mkdir /var/www/logs
RUN a2ensite apache
RUN a2enmod headers

# run apachea2
RUN a2dissite 000-default.conf
RUN a2ensite apache.conf

EXPOSE 80

WORKDIR /var/www

# copy application
COPY ./app ${APP_DIR}

CMD /usr/sbin/apache2ctl -D FOREGROUND