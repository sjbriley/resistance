# from channels.routing import ProtocolTypeRouter, route
# from resistance.consumers import ws_connect, ws_disconnect

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import online.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            online.routing.websocket_urlpatterns
        )
    ),
})