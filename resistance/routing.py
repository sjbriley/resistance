from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import online.routing

application = ProtocolTypeRouter({
    # AuthMiddlewareStack includes AuthMiddleware, SessionMiddleware, and CookieMiddleware
    # AllowedHostsOriginValidator only allows headers through ALLOWED_HOST or all if debug
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                online.routing.websocket_urlpatterns
            )
        ),
    ),
})