# -*- coding: utf-8 -*-
"""django-miniuser: URL configuration

Contains app specific URLs to decouple them from the project's URL config.

Please include
    url(r'^miniuser/', include('miniuser.urls')),
into your project's urls.py.

Please note, that with Django1.11, class based Login- and Logout-views have been
introduced. In order to be compatible with Django 1.10, some crazy and ugly
magic is applied here.

TODO: How does the namespacing or URLs work with different Django versions? (when was app_name introduced?)"""

# Django imports
from django.conf.urls import url

# app imports
from miniuser.views import MiniUserSignUpView

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
    url(r'^signup/$', MiniUserSignUpView.as_view(), name='signup'),
]
