#!/bin/sh

FILE=/etc/cron.d/sphinx_cron

echo '* * * * * root echo "Indexed $(date)" >> /var/log/cron.log 2>&1 && /usr/local/bin/indexer -c /etc/sphinxsearch/sphinx.conf --all --rotate --print-queries >> /var/log/cron.log 2>&1' > $FILE

chmod 0644 $FILE

crontab $FILE

cron

rm /var/lib/sphinxsearch/data/*

indexer -c /etc/sphinxsearch/sphinx.simple.conf --all

searchd -c /etc/sphinxsearch/sphinx.simple.conf --nodetach
