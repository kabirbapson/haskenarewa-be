import email
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import Follow, MyUser,  VerificationToken


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone_number', 'first_name',
                    'last_name', 'is_superuser')
    list_filter = ('is_superuser', 'email', 'phone_number',
                   'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('profile_picture', 'first_name',
         'last_name', 'phone_number', 'date_of_birth',)}),
        ('Activity', {'fields': ('likes', 'followers',)}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_superuser', 'is_verified')}),
        ('Important Date', {'fields': ('date_joined', 'last_login')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone_number', 'first_name', 'last_name',)
    ordering = ('-date_joined',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(VerificationToken)
admin.site.register(Follow)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
