from django.contrib import admin
from django.urls import path
from online import views as online_views
from django.conf.urls import include, url


urlpatterns = [
    path('', online_views.online_new, name='online_new'),
]