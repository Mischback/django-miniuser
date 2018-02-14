# -*- coding: utf-8 -*-
"""miniuser's models"""

# Python imports
from __future__ import unicode_literals

# Django imports
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class MiniUserManager(BaseUserManager):
    """Management class for MiniUser objects"""

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates a new user."""

        if not username:
            raise ValueError(_('The username must be set!'))

        if settings.MINIUSER_REQUIRE_VALID_EMAIL and not email:
            raise ValueError(_('The email address must be set!'))

        # normalize username and email
        username = self.model.normalize_username(username)
        email = self.normalize_email(email).lower()

        # apply the app setting, if the user is active on creation
        fields = {
            'is_active': settings.MINIUSER_DEFAULT_ACTIVE,
        }
        fields.update(extra_fields)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Creates a new superuser."""

        # apply the app setting, if the user is active on creation
        # Since this is a superuser, we hardcode an active account!
        # Furthermore, is_staff and is_superuser are set, this is taken from
        # Django's UserManager class.
        fields = {
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
        fields.update(extra_fields)

        user = self.create_user(username, email, password, **fields)

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
        if settings.MINIUSER_LOGIN_NAME == 'username':
            return self.get(username__iexact=input)
        if settings.MINIUSER_LOGIN_NAME == 'email':
            return self.get(email__iexact=input)


@python_2_unicode_compatible
class MiniUser(AbstractBaseUser, PermissionsMixin):
    """The user class extends the AbstractBaseUser and adds some custom fields
    to the default Django user."""

    username_validator = UnicodeUsernameValidator()
    """Make use of Django's built-in username validation"""

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or less.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists...')
        }
    )
    """The name of the user, that may be used for login. Must be unique"""

    email = models.EmailField(
        _('email address'),
        max_length=508,
        unique=True,
        blank=True,
        null=True,
        error_messages={
            'unique': _('This mail address is already in use....')
        }
    )
    """The email address of the user. Must be unique"""

    first_name = models.CharField(
        _('first name'),
        max_length=50,
        blank=True,
        help_text=_('Optional. 50 characters or less.')
    )
    """The first name of the user, optional."""

    last_name = models.CharField(
        _('last name'),
        max_length=50,
        blank=True,
        help_text=_('Optional. 50 characters or less.')
    )
    """The last name of the user, optional."""

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    """This flag indicates, if the user is active. Meaning: the user is able
    to log in."""

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    """This flag inidcates, if the user belongs to the site's staff and will
    be able to log into the admin part of Django."""

    email_is_verified = models.BooleanField(
        _('email verification status'),
        default=False,
        help_text=_('Designates whether the user already verified his mail address.')
    )

    registration_date = models.DateTimeField(
        _('date of registration'),
        default=timezone.now,
        editable=False
    )
    """The date of the registration. Will be set on account creation."""

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

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_username()
