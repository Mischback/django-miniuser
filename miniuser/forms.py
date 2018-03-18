# -*- coding: utf-8 -*-
"""django-miniuser: forms"""

# Django imports
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

# app imports
from miniuser.models import MiniUser


class MiniUserSignUpForm(UserCreationForm):
    """This extends Django's UserCreationForm to include app-specific options"""

    def __init__(self, *args, **kwargs):
        super(MiniUserSignUpForm, self).__init__(*args, **kwargs)

        if not settings.MINIUSER_REQUIRE_VALID_EMAIL:
            # self.fields[self._meta.model.EMAIL_FIELD].widget = HiddenInput()
            del self.fields[self._meta.model.EMAIL_FIELD]

    class Meta:
        model = MiniUser
        fields = (
            model.USERNAME_FIELD,
            model.EMAIL_FIELD,
            'password1', 'password2'
        )
