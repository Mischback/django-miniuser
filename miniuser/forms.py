# -*- coding: utf-8 -*-
"""django-miniuser: forms"""

# Django imports
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
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

        # Handle notifications in case of new signups
        if settings.MINIUSER_ADMIN_SIGNUP_NOTIFICATION:
            # superusers will be informed of this new registration!
            admin_mail_to = []
            admin_mail_subject = '[django-project] New User Signup'
            if (not settings.MINIUSER_DEFAULT_ACTIVE and not settings.MINIUSER_REQUIRE_VALID_EMAIL):
                # the new account will not be activated automatically!!!
                # TODO: Prepare a real mail body!
                admin_mail_text = 'Interaction Required: You have to activate an account!'
            else:
                # the new account will be activated automatically, following the process... (TODO)
                #   or is active by default.
                # TODO: Prepare a real mail body!
                admin_mail_text = 'Notification Mail; nothing to do!'

            # find all the admins, that want to receive a mail on signup
            # (heavily) relies on Django's ADMINS setting
            # TODO: In fact, this should not rely on ADMINS. In fact, these should
            #   be all 'superusers' and that may be bad for large projects aswell.
            #   Better would be, to dynamically detect, who is able to activate
            #   accounts or is responsible for this 'user management'.
            #   Database hits should be circumvented at any cost!
            for admin in settings.ADMINS:
                try:
                    if 'mail' in settings.MINIUSER_ADMIN_SIGNUP_NOTIFICATION[admin[0]]:
                        admin_mail_to.append(admin[1])
                except KeyError:
                    pass

            # send the admins
            if admin_mail_to:
                send_mail(
                    admin_mail_subject,
                    admin_mail_text,
                    None,
                    admin_mail_to,
                    fail_silently=False
                )

        return user         # pragma: nocover

    class Meta:
        model = MiniUser
        fields = (
            model.USERNAME_FIELD,
            model.EMAIL_FIELD,
            'password1', 'password2'
        )
