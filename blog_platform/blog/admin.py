from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Blog, Category

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
    form = BlogAdminForm
    list_display = ("id", "title", "author", "get_category", "status", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "author__username")
    readonly_fields = ("published_at",)  

    def get_category(self, obj):
        return obj.category.name if obj.category else "-"

    get_category.short_description = "Category"

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize form based on user role.
        - If the user is not a superuser, they cannot change 'status'.
        - The 'author' field is set to the logged-in user when creating a new blog.
        """
        form = super().get_form(request, obj, **kwargs)
        
        if not request.user.is_superuser:  
            form.base_fields["status"].disabled = True  
            if not obj:  
                form.base_fields["author"].initial = request.user
                form.base_fields["author"].disabled = True  
        
        return form
