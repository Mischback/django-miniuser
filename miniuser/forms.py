# -*- coding: utf-8 -*-
"""django-miniuser: forms"""

# Django imports
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

# app imports
from miniuser.models import MiniUser


class MiniUserSignUpForm(UserCreationForm):
    """This extends Django's UserCreationForm to include app-specific options"""

    class Meta:
        model = MiniUser

        if settings.MINIUSER_REQUIRE_VALID_EMAIL:
            fields = ('username', 'email', 'password1', 'password2')
        else:
            fields = ('username', 'password1', 'password2')
