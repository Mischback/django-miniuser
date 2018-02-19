# -*- coding: utf-8 -*-

# Django imports
from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('miniuser.urls')),
]
