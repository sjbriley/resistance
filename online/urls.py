from django.contrib import admin
from django.urls import path
from . import views as online_views
from django.conf.urls import include, url


urlpatterns = [
    path('', online_views.home_online, name='home_online'),
    path('new_game/', online_views.online_game_set_up, name='online_game_set_up'),
    path('game/<str:game_id>', online_views.online_game, name="online_game"),
]