from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {'fields': ('phone', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('user_info'), {'fields': (
            'email', 'gender', 'date_of_birth', 'profile_picture', 'nid_number', 'nid_file', 'country', 'division',
            'district', 'area', 'sub_area', 'short_address', 'zip_code', 'role', 'is_verified',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    list_display = ['phone', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ('phone', 'email', 'first_name', 'last_name')
    ordering = ('phone',)
