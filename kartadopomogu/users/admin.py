from django.contrib import admin
from .models import UserModel


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main', {'fields': ['first_name', 'last_name', 'email', 'password', 'username']}),
        ('Addition', {'fields': ['phone_number', 'bio', 'status', 'avatar', 'is_verified']}),
        ('Permissions', {'fields': ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active']}),
    ]
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'status', 'is_verified')
    list_display_link = ('id', 'username')  #???
    search_fields = ('user_name', 'status', 'is_verified')#???


admin.site.register(UserModel, UserAdmin)
