from django.contrib import admin
from account.models import Customer, Address
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address


class UserAdmin(DefaultUserAdmin):
    model = Customer
    filter_horizontal = ('addresses',)

    list_display = (
        'username', 'first_name', 'last_name', 'email', 'phone', 'is_superuser', 'is_staff', 'is_active',
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
         'fields': (('first_name', 'last_name'), 'email', 'phone', 'addresses')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Address)
admin.site.register(Customer, UserAdmin)
