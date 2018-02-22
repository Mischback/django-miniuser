# -*- coding: utf-8 -*-
"""MiniUser URL configuration

Contains app specific URLs to decouple them from the project's URL config.

Please include
    url(r'^miniuser/', include('miniuser.urls')),
into your project's urls.py."""

# Django imports
from django.conf.urls import url
try:
    # Django > 1.10
    from django.contrib.auth.views import LoginView, LogoutView

    def login_view():
        """Returns an url-statement using class-based views"""
        return url(r'^login/$', LoginView.as_view(template_name='miniuser/login.html'), name='login')

    def logout_view():
        """Returns an url-statement using class-based views"""
        return url(r'^logout/$', LogoutView.as_view(template_name='miniuser/logout.html'), name='logout')

except ImportError:
    # Django <= 1.10
    from django.contrib.auth.views import login, logout

    def login_view():
        """Returns an url-statement using function-based views"""
        return url(r'^login/$', login, {'template_name': 'miniuser/login.html'}, name='login')

    def logout_view():
        """Returns an url-statement using function-based views"""
        return url(r'^logout/$', logout, {'template_name': 'miniuser/logout.html'}, name='logout')


app_name = 'miniuser'
urlpatterns = [
    login_view(),
    logout_view(),
]
