FROM ubuntu:16.04 as sphinx


RUN apt-get update && \
    apt-get -y install wget gcc g++ make libpq-dev libpqxx-dev postgresql libmysql++ mysql-client && \
    apt-get -y install cron && \
    mkdir -p /var/log/sphinxsearch && \
    mkdir -p /var/run/sphinxsearch && \
    mkdir -p /var/lib/sphinxsearch/data && \
    touch /var/log/sphinxsearch/searchd.log && \
    touch /var/log/sphinxsearch/query.log && \
    touch /var/run/sphinxsearch/searchd.pid && \
    ln -sf /dev/stdout /var/log/sphinxsearch/searchd.log && \
    ln -sf /dev/stderr /var/log/sphinxsearch/query.log && \
    wget https://github.com/sphinxsearch/sphinx/archive/2.3.2-beta.tar.gz && \
    tar xzvf /2.3.2-beta.tar.gz && \
    rm /2.3.2-beta.tar.gz && \
    touch /var/log/cron.log

WORKDIR /sphinx-2.3.2-beta

RUN ./configure \
    --with-mysql \
    --with-pgsql=/usr/lib/postgresql/9.5/lib \
    --with-pgsql-includes=/usr/include/postgresql \
    --with-pgsql-libs && \
    make && \
    make install

RUN apt-get -y remove g++ gcc wget make

FROM sphinx

# TODO: setup for delta and main index using volumes
# ADD crontab /etc/cron.d/sphinx_cron

# RUN chmod 0644 /etc/cron.d/sphinx_cron

COPY sphinx.conf /etc/sphinxsearch/sphinx.conf
COPY run.simple.sh /etc/sphinxsearch/run.simple.sh

VOLUME ["/etc/sphinxsearch"]

EXPOSE 9306

CMD "/etc/sphinxsearch/run.simple.sh"
