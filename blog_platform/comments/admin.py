from django.contrib import admin
from .models import Comment


@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "user", "content", "is_approved", "created_at")
    search_fields = ("user__user__username", "blog__title", "content")
    list_filter = ("is_approved", "created_at")
    ordering = ("-created_at",)
    actions = ["approve_comments"]


    def approve_comments(self, request, queryset):
     queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"


