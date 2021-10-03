from django.urls import re_path
from django.conf.urls import url
from online import online_consumers
from local import local_consumers

websocket_urlpatterns = [
    re_path(r'online/ws/(?P<game_id>\w+)/$', online_consumers.GameConsumer.as_asgi()),
    re_path(r'local/ws/(?P<game_id>\w+)/$', local_consumers.GameConsumer.as_asgi()),
]