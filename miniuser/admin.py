# -*- coding: utf-8 -*-
"""miniuser's admin integration"""

# Django imports
from django.conf import settings
from django.contrib import admin
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
            'email',
            'email_is_verified',
            'status_aggregated',
            'last_login',
        )
        # if this statement is reached, inject this setting now at last!
        setattr(settings, 'MINIUSER_ADMIN_LIST_DISPLAY', list_display)

    # controls, which fields are used to access the objects detail view
    # list_display_links

    # controls, which fields are editable in the list view
    # list_editable = ('is_active',)

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
            search_fields = ('username', 'email', 'first_name', 'last_name')
            setattr(settings, 'MINIUSER_ADMIN_SHOW_SEARCHBOX', True)
    except AttributeError:
        setattr(settings, 'MINIUSER_ADMIN_SHOW_SEARCHBOX', False)

    # admin actions
    actions = ['action_activate_user', 'action_deactivate_user']

    def get_actions(self, request):
        """Override the default get_actions()-method to exclude delete objects"""

        # get the original list of actions
        actions = super().get_actions(request)

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
