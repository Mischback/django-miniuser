# -*- coding: utf-8 -*-

# Django imports
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('miniuser.urls')),
    url(r'^admin/', admin.site.urls),
]
