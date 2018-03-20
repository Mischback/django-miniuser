# -*- coding: utf-8 -*-
"""django-miniuser Admin integration

This file provides all specific classes and functions, that are used in Django's
admin backend."""

# Django imports
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.contrib.messages import ERROR, SUCCESS, WARNING
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# app imports
from .exceptions import MiniUserObjectActionException
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
            'toggle_is_active',
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
    actions = ['action_bulk_activate_user', 'action_bulk_deactivate_user']

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

    def changelist_view(self, request, extra_context=None):
        """Override changelist_view()-method to pass some more context to the view

        This is used to:
            - provide the legend (at the foot of the list view)"""

        extra_context = extra_context or {}
        extra_context['miniuser_legend'] = self.get_miniuser_legend()

        return super(MiniUserAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        """Override get_urls()-method to include our custom admin actions and
        make them accessible with a single button."""

        urls = super(MiniUserAdmin, self).get_urls()

        # TODO: Write tests for this override!
        custom_urls = [
            url(
                r'^(?P<user_id>.+)/activate/$',
                self.admin_site.admin_view(self.action_activate_user),
                name='miniuser-activate-user'
            ),
            url(
                r'^(?P<user_id>.+)/deactivate/$',
                self.admin_site.admin_view(self.action_deactivate_user),
                name='miniuser-deactivate-user'
            ),
        ]

        return custom_urls + urls

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

    def toggle_is_active(self, obj):
        """Shows a button to activate or deactivate an account, depending on
        'is_active'

        TODO: Write tests for this method!"""

        if obj.is_active:
            # show deactivate button
            button = format_html(
                '<a href="{}" class="button">deactivate</a>'.format(
                    reverse('admin:miniuser-deactivate-user', args=[obj.pk])
                )
            )
        else:
            # show activate button
            button = format_html(
                '<a href="{}" class="button">activate</a>'.format(
                    reverse('admin:miniuser-activate-user', args=[obj.pk])
                )
            )

        return button
    toggle_is_active.short_description = _('Modify activation status')

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

    def action_bulk_activate_user(self, request, queryset):
        """Performs bulk activation of users in Django admin

        This action is accessible from the drop-down menu and works together
        with selecting user objects by checking their respective checkbox.

        TODO: Is it necessary to check REQUIRE_VALID_EMAIL? Currently it is
            possible to activate accounts, even if they have no verified mail
            and the app's settings do require them."""

        updated = queryset.update(is_active=True)

        if updated == 1:
            msg = _('1 user was activated successfully.')
        else:
            msg = _('{} users were activated successfully.'.format(updated))
        self.message_user(request, msg)
    action_bulk_activate_user.short_description = _('Activate selected users')

    def action_bulk_deactivate_user(self, request, queryset):
        """Performs bulk deactivation of users in Django admin

        This action is accessible from the drop-down menu and works together
        with selecting user objects by checking their respective checkbox.

        TODO: Ensure, that the admin CAN NOT deactivate himself!"""

        updated = queryset.update(is_active=False)

        if updated == 1:
            msg = _('1 user was deactivated successfully.')
        else:
            msg = _('{} users were deactivated successfully.'.format(updated))
        self.message_user(request, msg)
    action_bulk_deactivate_user.short_description = _('Deactivate selected users')

    def action_activate_user(self, request, user_id, *args, **kwargs):
        """This action activates an user-object in Django admin

        This action is accessible as a button per object row and will activate
        only that single user.

        TODO: Here, server state is modified by a GET-request. *fubar*"""

        user = self.get_object(request, user_id)

        # try to activate the user. Checking of constraints will happen in
        # the model-class.
        try:
            user.activate_user()
            self.message_user(
                request,
                _('User {} was successfully activated.'.format(user.username)),
                SUCCESS,
            )
        except AttributeError:
            self.message_user(
                request,
                _('No User object with the given id ({}) found!'.format(user_id)),
                ERROR,
            )
        except MiniUserObjectActionException:
            self.message_user(
                request,
                _('User {} could not be activated, because his email address is not verified!'.format(user.username)),
                ERROR,
            )
        return redirect(reverse('admin:miniuser_miniuser_changelist'))

    def action_deactivate_user(self, request, user_id, *args, **kwargs):
        """This action deactivates an user-object in Django admin

        This action is accessible as a button per object row and will deactivate
        only that single user.

        TODO: Here, server state is modified by a GET-request. *fubar*"""

        user = self.get_object(request, user_id)

        # try to deactivate the user. Checking of constraints will happen in
        # the model-class.
        try:
            user.deactivate_user(request_user=request.user)
            self.message_user(
                request,
                _('User {} was successfully deactivated.'.format(user.username)),
                SUCCESS,
            )
        except AttributeError:
            self.message_user(
                request,
                _('No User object with the given id ({}) found!'.format(user_id)),
                ERROR,
            )
        except MiniUserObjectActionException:
            self.message_user(
                request,
                _('You may not deactivate your own account!'),
                WARNING,
            )
        return redirect(reverse('admin:miniuser_miniuser_changelist'))
