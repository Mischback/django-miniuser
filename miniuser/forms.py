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

        if settings.MINIUSER_ADMIN_SIGNUP_NOTIFICATION:
            # TODO: Write tests targeting this bunch of code!
            # superusers will be informed of this new registration!
            admin_mail_to = []
            admin_mail_subject = '[django-project] New User Signup'
            if settings.MINIUSER_REQUIRE_VALID_EMAIL or settings.MINIUSER_DEFAULT_ACTIVE:
                # the new account will be activated automatically, following the process... (TODO)
                # the admin will only need an information mail
                admin_mail_text = 'foo'
            elif not settings.MINIUSER_DEFAULT_ACTIVE:
                # the new accoutn will not be activated automatically!!!
                # shall we send an email to the admins? Or notify with another method?
                admin_mail_text = 'bar'

            # find all the admins, that want to receive a mail on signup
            # TODO: THIS IS REALLY BAD! For creating a user, several hits on the database are needed to grab the
            #   admin's email addresses. This is just a big fuck up!
            #   The validity of admin-addresses can't be handled in app-specific checks, because these checks are
            #   executed before the models are accessible, but this would be the place to do so.
            #   Probably it would be best to rely on Django's ADMINS-setting. We will shift the responsibility to the
            #   admin of the project. In fact, he would be the one to fill our own setting aswell.
            for username in settings.MINIUSER_ADMIN_SIGNUP_NOTIFICATION:
                tmp = MiniUser.objects.get(username=username)
                if 'mail' in settings.MINIUSER_ADMIN_SIGNUP_NOTIFICATION[username]:
                    admin_mail_to.append(tmp.email)

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
