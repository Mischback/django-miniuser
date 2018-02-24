# -*- coding: utf-8 -*-
"""miniuser's admin integration"""

# Django imports
from django.contrib import admin

# app imports
from .models import MiniUser, MiniUserAdmin

admin.site.register(MiniUser, MiniUserAdmin)
