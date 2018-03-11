App-specific Settings
=====================

**django-miniuser** lets you control its features with your project's Django
settings module. This section of the documentation lists the available options
with their respective default.

To alter the settings, simply include them in your settings module. As with
Django's settings, setting names have to be written in capitals.

**django-miniuser** will automatically check your settings for validity.

Available Settings
------------------

.. glossary::

    ``MINIUSER_DEFAULT_ACTIVE``
        Controls, if newly registered users will be activated by default.

        Accepted values: ``True``, ``False`` (default: ``True``)

    ``MINIUSER_LOGIN_NAME``
        Controls, if the username or the email address is used to login.

        Accepted values: ``'username'``, ``'email'``, ``'both'`` (default: ``'username'``)

    ``MINIUSER_REQUIRE_VALID_EMAIL``
        Controls, if the users require a valid email address.

        Accepted values: ``True``, ``False`` (default: ``False``)

    ``MINIUSER_ADMIN_LIST_DISPLAY``
        This setting is used in Django's admin interface and controls, which
        fields are displayed in Miniuser's list view.

        Basically, every attribute of the User-objects can be accessed, but
        additionally, some enhanced fields are available. See the following list
        for accepted values:

        * ``'username_color_status'``: the usernames, colorized according to their status (see ``MINIUSER_ADMIN_STATUS_COLOR_STAFF`` and ``MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER``)
        * ``'username_character_status'``: the usernames, marked with an additional character to mark their status (see ``MINIUSER_ADMIN_STATUS_CHAR_STAFF`` and ``MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER``)
        * ``'username'``: the default Django username
        * ``'email'``: the user's email address (please note, that this may be empty)
        * ``'first_name'``: the user's first name (please note, that this may be empty)
        * ``'last_name'``: the user's last name (please note, that this may be empty)
        * ``'status_aggregated'``
        * ``'is_active'``: an icon, representing the activation status
        * ``'is_staff'``: an icon, representing if the user is staff-member
        * ``'is_superuser'`` an icon, representing if the user is superuser
        * ``'email_is_verified'`` an icon, representing if the user's email address was verified
        * ``'last_login'``: the date and time of the user's last login
        * ``'registration_date'``: the date and time of the user's registration
        * ``'email_with_status'``: field that combines the user's email address with the corresponding validation status

        You can combine any of these options into a customized view by simply
        specifying a Python list/tuple as value of this setting
        (default: ``('username_color_status', 'email_with_status', 'is_active', 'last_login')``).

    ``MINIUSER_ADMIN_SHOW_SEARCHBOX``
        This setting is used in Django's admin interface and controls, if a
        searchbox is displayed in MiniUser's list view.

        Accepted values: ``True``, ``False`` (default: ``False``)

    ``MINIUSER_ADMIN_STATUS_COLOR_STAFF``
        This setting is used in Django's admin interface and determines the
        color to mark staff users (by coloring their usernames).

        Accepted values: any hexadecimal color code like ``#rrggbb``. Please note
        the leading '#' (default: ``'#00cc00'``).

    ``MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER``
        This setting is used in Django's admin interface and determines the
        color to mark superusers (by coloring their usernames).

        Accepted values: any hexadecimal color code like ``#rrggbb``. Please note
        the leading '#' (default: ``'#cc0000'``).

    ``MINIUSER_ADMIN_STATUS_CHAR_STAFF``
        This setting is used in Django's admin interface and determines the
        character, that is used to mark staff users (by prefixing their names
        with '[:c:]', where ``:c:`` is the specified character).

        Accepted values: any single character (default: ``'$'``)

    ``MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER``
        This setting is used in Django's admin interface and determines the
        character, that is used to mark superusers (by prefixing their names
        with '[:c:]', where ``:c:`` is the specified character).

        Accepted values: any single character (default: ``'#'``)


Relevant Django settings
------------------------

In addition to the app specific settings, **django-miniuser** relies on certain
Django built-in settings. The app will automatically check these settings
aswell, because they are used throughout the app.

.. glossary ::

    ``AUTH_USER_MODEL``
        This setting has to be set to **django-miniuser**'s MiniUser class,
        which will handle authentication-related functions.

        Currently, Django's check-framework will raise an error and present an
        error message to the user. This will be further evaluated, especially
        to give the user some more freedom, in what to do about his user model.

        Accepted values: 'miniuser.MiniUser' (default: 'miniuser.MiniUser')


Developer's Description
-----------------------

There are two different techniques used, to inject **django-miniuser**'s
settings into the project.

By default, app-specific settings are checked in the ``AppConfig ready()``-method.
Because some parts of the application rely on the settings, they will be
injected into Django's settings module at runtime (Yes, this *is* discouraged by
Django's documentation, but is easily the best way to provide sane default
values for application specific settings).

However: This is not doable for settings, that are accessed before the
application's ``ready()``-method is executed, i.e. some settings to control the
behaviour of the admin interface.

If you want to mess with these internals, here is a documentation of where the
default values are injected, if not in ``apps.py``:

* ``MINIUSER_ADMIN_LIST_DISPLAY`` - admin.py
* ``MINIUSER_ADMIN_SHOW_SEARCHBOX`` - admin.py
