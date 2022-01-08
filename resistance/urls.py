"""resistance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from online import views as online_views
from django.conf.urls import include, url
import online.urls as online_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', online_views.home_page, name='home_page'),
    url(r'^accounts/', include("django.contrib.auth.urls")),
    url(r'^online/', include(online_urls)),
    path('accounts/sign_up', online_views.sign_up, name="sign_up"),
    path('my_account', online_views.my_account, name="my_account"),
    path('leaderboards', online_views.leaderboards, name="leaderboards"),
    path('about', online_views.about, name="about"),
    path('game_information/', online_views.game_information, name="game_information"),
    path('game_information/roles', online_views.role_information, name="role_information"),
]
