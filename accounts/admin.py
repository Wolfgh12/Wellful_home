from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        'username', 
        'email', 
        'role', 
        'phone_number', 
        'digital_address', 
        'is_staff', 
        'is_superuser', 
        'is_active'
    ]
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'phone_number', 'digital_address']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Wellful Home Profile', {
            'fields': ('role', 'phone_number', 'digital_address')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Wellful Home Profile', {
            'fields': ('role', 'phone_number', 'digital_address')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Non-superusers (Employee Admins) cannot modify authorization levels or critical flags
        if not request.user.is_superuser:
            return (
                'is_superuser', 
                'is_staff', 
                'groups', 
                'user_permissions', 
                'role', 
                'last_login', 
                'date_joined'
            )
        return super().get_readonly_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Only Supreme Super Admin can delete user accounts
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)