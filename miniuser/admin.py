# -*- coding: utf-8 -*-
"""miniuser's admin integration"""

# Django imports
from django.contrib import admin

# app imports
from .models import MiniUser


@admin.register(MiniUser)
class MiniUserAdmin(admin.ModelAdmin):
    """Represents MiniUser in Django's admin interface"""
    pass
