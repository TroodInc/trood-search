# Trood search

## Index configuration

1. start docker container (docker-compose up -d)
2. run this command in container "printenv >> /etc/environment && cron && tail -f /var/log/cron.log"

See examples in sphinxsearch folder.

## Testing

```bash
make
cd search
make test
```

## Versioning

Use [Semantic Versioning](https://semver.org/)