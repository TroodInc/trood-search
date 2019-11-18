import pathlib

from envparse import ConfigurationError, Env


def setup():
    env = Env(
        DEBUG=(bool, False),

        HOST=(str, '0.0.0.0'),
        PORT=(int, 8080),

        SECRET_KEY=(str, '548ab8296ff44d2f954c17d850833af1'),

        SPHINX_URL=(str, 'http://sphinxsearch:9307/'),
        SPHINX_DSN=(str, 'mysql://sphinxsearch:9306/'),
        SEARCH_INDEXES=(str, ''),

        AUTH_URL=(str, 'http://auth:8000/'),
        AUTH_DOMAIN=(str, 'SEARCH'),
        AUTH_SECRET=(str, 'b1b4a229c0cb5865f67f0626dc9c184526dc6dd99f8f505b14d1c95739d523dfcfaa17534ea160364fe27e10e6c331a1c231f60be581e69fed4f5bf9c4dfdadb'),
        EXCEPT_URLS=(str, '/ping/,/'),

        SENTRY_ENABLED=(bool, False),
        SENTRY_DSN=(str, 'https://42d08b480e6c4171a19c5c61cea98c0f:4bfb7897b15a4df4b31133bd02d8aff3@sentry.tools.trood.ru/5'),
    )
    env.read_envfile(pathlib.Path.cwd() / '.env')
    settings = Settings(env)
    return settings


class Settings:
    def __init__(self, env):
        for key, item in env.schema.items():
            self._set_attr(env, key, item)

    def _set_attr(self, env, key, value):
        _class, default = value
        try:
            value = getattr(env, _class.__name__)(key)
        except ConfigurationError:
            value = default

        setattr(self, key, value)
