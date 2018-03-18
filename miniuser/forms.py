# -*- coding: utf-8 -*-
"""django-miniuser: forms"""

# Django imports
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

# app imports
from miniuser.models import MiniUser


class MiniUserSignUpForm(UserCreationForm):
    """This extends Django's UserCreationForm to include app-specific options"""

    def __init__(self, *args, **kwargs):
        """Custom constructor to remove unnecessary fields from the form.

        Removing of fields depends on application specific settings."""

        # always call the parent constructor
        super(MiniUserSignUpForm, self).__init__(*args, **kwargs)

        # if the email address is not mandatory, remove it from the form
        if not settings.MINIUSER_REQUIRE_VALID_EMAIL:
            del self.fields[self._meta.model.EMAIL_FIELD]

    def clean(self):
        """Custom validation

        Apply some logical constraints on the user's input, depending on
        app specific settings."""

        # grab data
        cleaned_data = super(MiniUserSignUpForm, self).clean()

        email = cleaned_data.get(self._meta.model.EMAIL_FIELD)
        if settings.MINIUSER_REQUIRE_VALID_EMAIL and not email:
            # TODO: How to display this validation error?
            raise ValidationError(
                _('A valid email address is required!'),
                code='valid_email_required')

        return cleaned_data

    def save(self, commit=True):
        """Overrides the save()-method to include our model-specific clean()"""

        user = super(MiniUserSignUpForm, self).save(commit=False)

        # apply the user-object's constraints
        user.clean()

        if commit:          # pragma: nocover
            user.save()     # pragma: nocover
        return user         # pragma: nocover

    class Meta:
        model = MiniUser
        fields = (
            model.USERNAME_FIELD,
            model.EMAIL_FIELD,
            'password1', 'password2'
        )
