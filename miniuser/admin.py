# -*- coding: utf-8 -*-
"""miniuser's admin integration"""

# Django imports
from django.contrib import admin
from django.utils.html import format_html

# app imports
from .models import MiniUser


class MiniUserAdminStaffStatusFilter(admin.SimpleListFilter):
    """Custom SimpleListFilter to filter on user's status"""

    # the title of this filter
    title = 'status'

    # the parameter in the URL
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Controls the options in the filter list

        First value in the tuple: parameter in the query string
        Second value: The caption for the filter list"""

        # TODO: localize this
        return (
            ('users', 'Users'),
            ('staff', 'Staff'),
            ('superusers', 'Superusers')
        )

    def queryset(self, request, queryset):
        """How to modify the queryset for this filter"""

        if self.value() == 'users':
            return queryset.filter(is_staff=False).filter(is_superuser=False)

        if self.value() == 'staff':
            return queryset.filter(is_staff=True)

        if self.value() == 'superusers':
            return queryset.filter(is_superuser=True)


@admin.register(MiniUser)
class MiniUserAdmin(admin.ModelAdmin):
    """Represents MiniUser in Django's admin interface"""

    # controls, which fields are displayed in the list overview
    list_display = (
        'username_color_status',
        'username_character_status',
        'username',
        'email',
        'first_name',
        'last_name',
        'status_aggregated',
        'is_active',
        'is_staff',
        'is_superuser',
        'email_is_verified',
        'last_login',
        'registration_date',
    )

    # controls, which fields are used to access the objects detail view
    # list_display_links

    # controls, which fields are editable in the list view
    # list_editable = ('is_active',)

    # controls the applicable filters
    list_filter = ('is_active', MiniUserAdminStaffStatusFilter)

    # controls the default ordering of the list view
    ordering = ('-is_superuser', '-is_staff', 'is_active', 'username')

    # enables a searchbox and specifies, which fields are used for the search
    search_fields = ('username', 'email')

    def status_aggregated(self, obj):
        """Returns the status of the user"""

        # TODO: Localize these!
        status = 'user'
        if obj.is_superuser:
            status = 'superuser'
        elif obj.is_staff:
            status = 'staff'

        return status
    status_aggregated.short_description = 'Status'

    def username_color_status(self, obj):
        """Returns a colored username according to his status (HTML)"""

        # TODO: Make this hardcoded values configurable within settings
        if obj.is_superuser:
            color = '#cc0000'
        elif obj.is_staff:
            color = '#00cc00'
        else:
            return obj.username

        return format_html('<span style="color: {};">{}</span>', color, obj.username)
    username_color_status.short_description = 'Username (status)'
    username_color_status.admin_order_field = '-username'

    def username_character_status(self, obj):
        """Returns the prefixed username with status indicating characters"""

        # TODO: Make this hardcoded values configurable in settings
        if obj.is_superuser:
            status = '#'
        elif obj.is_staff:
            status = '~'
        else:
            return obj.username

        return '[{}] {}'.format(status, obj.username)
    username_character_status.short_description = 'Username (status)'
    username_character_status.admin_order_field = 'username'
