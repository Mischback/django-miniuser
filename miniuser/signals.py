# -*- coding: utf-8 -*-
"""django-miniuser: Signal handling

This file contains everything dealing with Django's signal system."""


def callback_user_logged_in(sender, user, **kwargs):
    """This function triggers certain tasks, when an user has authenticated."""

    # update timestamp for last_login field
    # TODO: This is automatically done by Django, though no documentation could
    #   be found...
    user.update_last_login()
