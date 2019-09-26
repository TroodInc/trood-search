# Trood search REST API server

## Description

Part of search server. Proxy request from http clients to Sphinx search engine.

## Run

```bash
make run
```

## API

```bash
curl -X GET http://search-api-host/?index=trood&match=search&select=id,title,product&group=product,order_by=id desc,limit=5
```
