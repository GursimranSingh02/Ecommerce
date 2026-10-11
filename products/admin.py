from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "name", "is_staff", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "createdAt", "updatedAt")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    readonly_fields = ("createdAt", "updatedAt", "last_login")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inStock", "createdAt", "updatedAt")
    list_filter = ("inStock",)
