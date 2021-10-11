from django.urls import re_path
from django.conf.urls import url
from . import online_consumers

websocket_urlpatterns = [
    re_path(r'online/ws/(?P<game_id>\w+)/$', online_consumers.GameConsumer.as_asgi()),
]