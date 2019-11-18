# Trood search

## Usage

```yml
version: "3"

services:

  search:
    image: registry.tools.trood.ru/search.tcp:dev
    container_name: search
    restart: always
    env_file:
      - ./search/.env
    environment:
      DEBUG: "False"
      HOST: "0.0.0.0"
      PORT: 8080
      SECRET_KEY: "548ab8296ff44d2f954c17d850833af1"
      SPHINX_URL: "http://sphinxsearch:9307/"
      AUTH_URL: "http://auth.trood.com/"
      AUTH_DOMAIN: "SEARCH"
      AUTH_SECRET: "b1b4a229c0cb5865f67f0626dc9c184526dc6dd99f8f505b14d1c95739d523dfcfaa17534ea160364fe27e10e6c331a1c231f60be581e69fed4f5bf9c4dfdadb"
      SENTRY_ENABLED: "False"
      SENTRY_DSN: "https://42d08b480e6c4171a19c5c61cea98c0f:4bfb7897b15a4df4b31133bd02d8aff3@sentry.tools.trood.ru/5"
    networks:
      - search_net
    ports:
      - "8030:8080"
  
  sphinxsearch:
    image: registry.tools.trood.ru/sphinxsearch.tcp:dev
    container_name: sphinxsearch
    restart: always
    volumes:
      - ./sphinxsearch/sphinx.conf:/etc/sphinxsearch/sphinx.conf
      - ./sphinxsearch/data:/var/lib/sphinxsearch/data
    networks:
      - search_net
    ports:
      - "9307:9307"

networks:
  search_net:
    driver: bridge

```

## Run

```bash
make run

```

## Query

```bash
curl -X GET 'http://search-host/?index=INDEX&match=SEARCH&select=id,title,category_id,dateadd&group=category_id,order_by=dateadd desc,limit=5'
```

## Поиск по PDF, DOC, XLS, ODF и подобным

Источник для Sphinx [xmlpipe2](http://sphinxsearch.com/docs/current/xmlpipe2.html)
