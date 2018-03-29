# -*- coding: utf-8 -*-
"""django-miniuser: Model definitions"""

from __future__ import unicode_literals

# Django imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# app imports
from .exceptions import (
    MiniUserActivateWithoutVerifiedEmailException,
    MiniUserConfigurationException, MiniUserDeactivateOwnAccountException,
)


class MiniUserManager(BaseUserManager):
    """Management class for MiniUser objects"""

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Creates a new user."""

        if not username:
            raise ValueError(_('The username must be set!'))

        if settings.MINIUSER_REQUIRE_VALID_EMAIL and not email:
            raise ValueError(_('The email address must be set!'))

        # normalize username and email
        username = self.model.normalize_username(username)
        email = self.normalize_email(email).lower().strip()

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        # apply MINIUSER_DEFAULT_ACTIVE
        user.is_active = settings.MINIUSER_DEFAULT_ACTIVE

        # set the password
        # TODO: Is some sort of validation included?
        user.set_password(password)

        # last time cleaning
        user.clean()

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Creates a new superuser."""

        user = self.create_user(username, email, password, **extra_fields)

        # apply the app setting, if the user is active on creation
        # Since this is a superuser, we hardcode an active account!
        # Furthermore, is_staff and is_superuser are set, this is taken from
        # Django's UserManager class.
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        # and now finally save the superuser
        user.save()

        return user

    def get_by_natural_key(self, input):
        """Retrieves a single user by a unique field.

        This method is used during Django's authentication process to retrieve
        the user. See django.contrib.auth.backends ModelBackend class.

        Depending on the app's settings, the user-object can be retrieved by
        its username, its mail address or both."""

        if settings.MINIUSER_LOGIN_NAME == 'both':
            try:
                user = self.get(username__iexact=input)
            except MiniUser.DoesNotExist:
                user = self.get(email__iexact=input)
                # TODO: ok, the email is now used just like a username. Is this correct?
                #   Shouldn't the email be validated to be used as username?
            return user
        elif settings.MINIUSER_LOGIN_NAME == 'username':
            return self.get(username__iexact=input)
        elif settings.MINIUSER_LOGIN_NAME == 'email':
            return self.get(email__iexact=input)
        else:
            # if this exception is raised, apps.py:check_correct_values() failed or was not executed!
            raise MiniUserConfigurationException(_("'MINIUSER_LOGIN_NAME' has an undefined value!"))


class MiniUser(AbstractUser):
    """The user class extends the AbstractBaseUser and adds some custom fields
    to the default Django user."""

    email = models.EmailField(
        _('email address'),
        max_length=508,
        unique=True,
        blank=True,
        null=True,
        default=None,
        error_messages={
            'unique': _('This mail address is already in use....')
        }
    )
    """The email address of the user. Must be unique"""

    email_is_verified = models.BooleanField(
        _('email verification status'),
        default=False,
        help_text=_('Designates whether the user already verified his mail address.')
    )

    # apply the MiniUserManager
    objects = MiniUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        """Provides some custom validation steps for MiniUser objects"""

        # ensure that an empty email will be stored as 'None'
        if self.email == '':
            self.email = None

        # deactivate user without usable passwords
        if not self.has_usable_password():
            self.is_active = False

    def activate_user(self):
        """Activates an account by setting 'is_active' = True"""

        if settings.MINIUSER_REQUIRE_VALID_EMAIL and not self.email_is_verified:
            raise MiniUserActivateWithoutVerifiedEmailException(
                _(
                    'You tried to activate an User-object, that has no '
                    'verified email address, but your project requires the '
                    'verification of email addresses.'
                )
            )

        if not self.is_active:
            self.is_active = True
            # TODO: Can this be optimised? Check model's save()-method!
            self.save()

    def deactivate_user(self, request_user=None):
        """Deactivates an account by setting 'is_active' = False"""

        # if this method is called from a view, ensure, that the requesting
        # user can not deactivate himself.
        if self == request_user:
            raise MiniUserDeactivateOwnAccountException(_('You can not deactivate yourself.'))

        if self.is_active:
            self.is_active = False
            # TODO: Can this be optimised? Check model's save()-method!
            self.save()
