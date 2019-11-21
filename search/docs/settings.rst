Settings
========

To setup application your can use environment variables or .env file.

You can setup next given variables:

.. envvar:: SPHINX_DB

    Host to search index db.
    
    Default: mysql://127.0.0.1:9306/

.. envvar:: AUTH_URL
    
    Host to `trood-auth` rest API.

    Default: http://auth:8000/

.. envvar:: AUTH_DOMAIN
    
    Service identification used in Trood Core ecosystem.

    Default: SEARCH

.. envvar:: AUTH_SECRET

    Random generated string for system token authentication purposes.

    Default: b1b4a229c0cb5865f67f0626dc9c184526dc6dd99f8f505b14d1c95739d523dfcfaa17534ea160364fe27e10e6c331a1c231f60be581e69fed4f5bf9c4dfdadb

.. envvar:: WHITE_URLS
    
    List of not protected pipelines.
    
    Default: 

.. envvar:: SENTRY_ENABLED

    Enable Sentry.io error collector.
    
    Default: False

.. envvar:: SENTRY_DSN
    
    Sentry.io DSN.

    Required if `SENTRY_ENABLED` is `True`.

    Default: https://42d08b480e6c4171a19c5c61cea98c0f:4bfb7897b15a4df4b31133bd02d8aff3@sentry.tools.trood.ru/5

