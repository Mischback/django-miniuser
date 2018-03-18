# -*- coding: utf-8 -*-
"""django-miniuser: forms"""

# Django imports
from django.contrib.auth.forms import UserCreationForm

# app imports
from miniuser.models import MiniUser


class MiniUserSignUpForm(UserCreationForm):
    """This extends Django's UserCreationForm to include app-specific options"""

    class Meta:
        model = MiniUser
        fields = ('username', 'password1', 'password2')
