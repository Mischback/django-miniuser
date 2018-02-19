# -*- coding: utf-8 -*-
"""MiniUser URL configuration

Contains app specific URLs to decouple them from the project's URL config.

Please include
    url(r'^miniuser/', include('miniuser.urls')),
into your project's urls.py."""

# Django imports
from django.conf.urls import url
from django.contrib.auth import views as auth_views


app_name = 'miniuser'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'miniuser/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
