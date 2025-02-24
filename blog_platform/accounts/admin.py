from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Reader


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = ("id", "username", "email", "bio", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_picture")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_picture")}),
    )


@admin.register(Reader)
class ReaderAdmin(UserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")  
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    filter_horizontal = ("favorite_categories",)  

    fieldsets = UserAdmin.fieldsets + (
        ("Preferences", {"fields": ("favorite_categories",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Preferences", {"fields": ("favorite_categories",)}),
    )
