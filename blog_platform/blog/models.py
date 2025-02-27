from django.db import models
from base.models import BaseModel
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.timezone import now

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Blog(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )  
    title = models.CharField(max_length=255, unique=True)
    content = CKEditor5Field("Content", config_name="default")
    author = models.ForeignKey("accounts.Author", on_delete=models.CASCADE)
    category = models.ForeignKey("blog.Category", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        """
        Ensure published_at is set only when status is 'published'.
        Prevents unauthorized direct publishing.
        """
        if self.status == "published" and not self.published_at:
            self.published_at = now()  
        elif self.status == "draft":
            self.published_at = None  
        
        super().save(*args, **kwargs)
