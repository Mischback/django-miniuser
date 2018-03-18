# -*- coding: utf-8 -*-
"""django-miniuser: Model definitions"""

from __future__ import unicode_literals

# Django imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# app imports
from .exceptions import MiniUserConfigurationException


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
        if email == '':
            email = None

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        # set the password
        # TODO: Is some sort of validation included?
        user.set_password(password)

        # apply the app's activation mode
        user.is_active = settings.MINIUSER_DEFAULT_ACTIVE

        # deactivate user without usable passwords
        if not user.has_usable_password():
            user.is_active = False

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

    last_login = models.DateTimeField(
        _('date of last login'),
        # TODO: will default to the account creation timestamp. Must be adjusted during login.
        default=timezone.now
    )
    """The date of the last login. Will be updated on every successfull login"""

    # apply the MiniUserManager
    objects = MiniUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def update_last_login(self):
        """Updates the timestamp of last login

        Is triggered by a signal, see apps.MiniUserConfig::ready() for details.

        Be aware: Django will automatically update a field called 'last_login',
        even if it is not part of Django's default user-model.

        TODO: Find Django's documentation, especially auth-app, where it's said,
            that Django will automatically update fields called 'last_login',
            even if Django's default user-model doesn't have that field!"""
        self.last_login = timezone.now()
        self.save()
