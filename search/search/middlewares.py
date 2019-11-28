import os

from starlette.middleware.errors import ServerErrorMiddleware
from starlette.types import Receive, Scope, Send


class SearchErrorMiddleware(ServerErrorMiddleware):
    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        try:
            return await super().__call__(scope, receive, send)
        except Exception as exc:
            if os.environ.get("SENTRY_ENABLED", True):
                import sentry_sdk

                sentry_sdk.init(
                    dsn=os.environ.get(
                        "SENTTRY_DSN",
                        "https://e596af21d20d4fca8867a727b0003b47:d9ae422ff66e42138fba31a64f1414eb@sentry.tools.trood.ru/7",
                    )
                )
                sentry_sdk.capture_exception(exc)

            if exc.__str__() == "DatabaseBackend is not running":
                # TODO: Remove. For backward compatibility with legacy settings now.
                return

            raise exc from None
