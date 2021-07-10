from django.urls import re_path
from django.conf.urls import url
from online import consumers

websocket_urlpatterns = [
    re_path(r'ws/sheet/(?P<gameID>\w+)/$', consumers.GameConsumer.as_asgi()),
]