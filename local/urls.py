from django.contrib import admin
from django.urls import path
from local import views as local_views
from django.conf.urls import include, url


urlpatterns = [
    path('', local_views.home_local, name='home_local'),
    path('new_game', local_views.local_game_set_up, name='local_game_set_up'),
    path('game/<str:game_id>', local_views.local_game, name="local_game"),
]