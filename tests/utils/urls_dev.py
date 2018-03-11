# -*- coding: utf-8 -*-
"""django-miniuser: Development/test URL configuration.

This file mimics a project's URL configuration, in order to run the app during
development and testing."""

# Django imports
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('miniuser.urls')),
    url(r'^admin/', admin.site.urls),
]
