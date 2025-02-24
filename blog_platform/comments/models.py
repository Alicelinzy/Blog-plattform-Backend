from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from base.models import BaseModel
from blog.models import Blog
from django_ckeditor_5.fields import CKEditor5Field

class Comment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ["author", "reader"]})
    user_id = models.PositiveIntegerField()
    user =GenericForeignKey("user_type", "user_id")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = CKEditor5Field(config_name="default")  
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        blog_title = self.blog.title if self.blog else "Unknown Blog"
        user_name = str(self.user) if self.user else "Anonymous"
        return f"{user_name} on {blog_title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"