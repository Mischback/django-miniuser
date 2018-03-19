# -*- coding: utf-8 -*-
"""django-miniuser: URL configuration

Contains app specific URLs to decouple them from the project's URL config.

Please include
    url(r'^miniuser/', include('miniuser.urls')),
into your project's urls.py."""

# Django imports
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

# app imports
from miniuser.views import MiniUserSignUpView

app_name = 'miniuser'
urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='miniuser/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='miniuser/logout.html'), name='logout'),
    url(r'^signup/$', MiniUserSignUpView.as_view(), name='signup'),
]
