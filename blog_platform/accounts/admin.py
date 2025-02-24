from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Reader


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "bio", "created_at", "updated_at")
    search_fields = ("user__name", "id")
    list_filter = ()

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ( "user",)  
    search_fields = ("user__name", "user__id")
    filter_horizontal = ("favorite_categories",)  