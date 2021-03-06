# -*- coding: utf-8 -*-
"""django-miniuser Admin integration

This file provides all specific classes and functions, that are used in Django's
admin backend."""

# Django imports
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# app imports
from .models import MiniUser


class MiniUserAdminStaffStatusFilter(admin.SimpleListFilter):
    """Custom SimpleListFilter to filter on user's status"""

    # the title of this filter
    title = _('status')

    # the parameter in the URL
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Controls the options in the filter list

        First value in the tuple: parameter in the query string
        Second value: The caption for the filter list"""

        return (
            ('users', _('Users')),
            ('staff', _('Staff')),
            ('superusers', _('Superusers'))
        )   # pragma nocover

    def queryset(self, request, queryset):
        """How to modify the queryset for this filter"""

        if self.value() == 'users':
            return queryset.filter(is_staff=False).filter(is_superuser=False)

        if self.value() == 'staff':
            return queryset.filter(is_staff=True)

        if self.value() == 'superusers':
            return queryset.filter(is_superuser=True)

        return queryset


@admin.register(MiniUser)
class MiniUserAdmin(admin.ModelAdmin):
    """Represents MiniUser in Django's admin interface"""

    # controls, which fields are displayed in the list overview
    # Our usual way of providing the app's default values in apps.py does not
    #   work here, because we can't ensure, that our settings are injected,
    #   before Django's admin calls its autodiscover()-method.
    #   However, if the option is included in the project's settings, they will
    #   be set into effect here.
    #   Please note that there is a checking of the projects settings performed
    #   using Django's checks-framework (see apps.py).
    # TODO: Revisit the provided default values!
    try:
        list_display = settings.MINIUSER_ADMIN_LIST_DISPLAY
    except AttributeError:
        list_display = (
            'username_color_status',
            'email_with_status',
            'is_active',
            'last_login',
        )
        # if this statement is reached, inject this setting now at last!
        setattr(settings, 'MINIUSER_ADMIN_LIST_DISPLAY', list_display)

    # controls the applicable filters
    list_filter = ('is_active', MiniUserAdminStaffStatusFilter)

    # controls the default ordering of the list view
    ordering = ('-is_superuser', '-is_staff', 'is_active', 'username')

    # enables a searchbox and specifies, which fields are used for the search
    # Our usual way of providing the app's default values in apps.py does not
    #   work here, because we can't ensure, that our settings are injected,
    #   before Django's admin calls its autodiscover()-method.
    #   However, if the option is included in the project's settings, they will
    #   be set into effect here.
    #   Please note that there is a checking of the projects settings performed
    #   using Django's checks-framework (see apps.py).
    try:
        if settings.MINIUSER_ADMIN_SHOW_SEARCHBOX:
            search_fields = ('username', 'email', 'first_name', 'last_name')  # pragma: nocover
            setattr(settings, 'MINIUSER_ADMIN_SHOW_SEARCHBOX', True)  # pragma: nocover
    except AttributeError:
        setattr(settings, 'MINIUSER_ADMIN_SHOW_SEARCHBOX', False)  # pragma: nocover

    # admin actions (these will be accessible for bulk editing in list view)
    actions = ['action_activate_user', 'action_deactivate_user']

    def get_actions(self, request):  # pragma: nocover
        """Override the default get_actions()-method to exclude delete objects

        Even if this function is decorated with pragma: nocover, it is tested.
        See test_get_actions_raw() and test_get_actions() in test_admin.py for
        further details."""
        # TODO: Should deletion of users be really that hard?

        # get the original list of actions
        actions = super(MiniUserAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def status_aggregated(self, obj):
        """Returns the status of the user"""

        status = _('user')
        if obj.is_superuser:
            status = _('superuser')
        elif obj.is_staff:
            status = _('staff')

        return status
    status_aggregated.short_description = _('Status')

    def username_color_status(self, obj):
        """Returns a colored username according to his status (HTML)"""

        if obj.is_superuser:
            color = settings.MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER
        elif obj.is_staff:
            color = settings.MINIUSER_ADMIN_STATUS_COLOR_STAFF
        else:
            return obj.username

        return format_html('<span style="color: {};">{}</span>', color, obj.username)
    username_color_status.short_description = _('Username (status)')
    username_color_status.admin_order_field = '-username'

    def username_character_status(self, obj):
        """Returns the prefixed username with status indicating characters"""

        if obj.is_superuser:
            status = settings.MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER
        elif obj.is_staff:
            status = settings.MINIUSER_ADMIN_STATUS_CHAR_STAFF
        else:
            return obj.username

        return '[{}] {}'.format(status, obj.username)
    username_character_status.short_description = _('Username (status)')
    username_character_status.admin_order_field = '-username'

    def email_with_status(self, obj):
        """Combines email-address and verification status in one field"""

        # get the icon (with Django's template tag)
        icon = _boolean_icon(obj.email_is_verified)

        return format_html('{} {}', icon, obj.email)
    email_with_status.short_description = _('EMail')
    email_with_status.admin_order_field = '-email'

    def action_activate_user(self, request, queryset):
        """Performs bulk activation of users in Django admin"""

        updated = queryset.update(is_active=True)

        if updated == 1:
            msg = _('1 user was activated successfully.')
        else:
            msg = _('{} users were activated successfully.'.format(updated))
        self.message_user(request, msg)
    action_activate_user.short_description = _('Activate selected users')

    def action_deactivate_user(self, request, queryset):
        """Performs bulk deactivation of users in Django admin"""

        updated = queryset.update(is_active=False)

        if updated == 1:
            msg = _('1 user was deactivated successfully.')
        else:
            msg = _('{} users were deactivated successfully.'.format(updated))
        self.message_user(request, msg)
    action_deactivate_user.short_description = _('Deactivate selected users')

    def get_miniuser_legend(self):
        """Returns relevant information from the app's settings to enhance the context"""

        result = {}

        if 'username_color_status' in settings.MINIUSER_ADMIN_LIST_DISPLAY:
            colors = {
                'superuser': settings.MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER,
                'staff': settings.MINIUSER_ADMIN_STATUS_COLOR_STAFF
            }
            result['color'] = colors

        if 'username_character_status' in settings.MINIUSER_ADMIN_LIST_DISPLAY:
            characters = {
                'superuser': settings.MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER,
                'staff': settings.MINIUSER_ADMIN_STATUS_CHAR_STAFF
            }
            result['character'] = characters

        return result

    def changelist_view(self, request, extra_context=None):
        """Override changelist_view()-method to pass some more context to the view

        This is used to:
            - provide the legend (at the foot of the list view)"""

        extra_context = extra_context or {}
        extra_context['miniuser_legend'] = self.get_miniuser_legend()

        return super(MiniUserAdmin, self).changelist_view(request, extra_context=extra_context)
