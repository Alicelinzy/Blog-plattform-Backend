from django.contrib import admin
from .models import Blog, Category
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(config_name="default"),  
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Blog)

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "get_category", "status", "published_at")  
    list_filter = ("status","category")  
    search_fields = ("title", "author__username")

    def get_category(self, obj):
        return obj.category.name if obj.category else "-"
    
    get_category.short_description = "Category"