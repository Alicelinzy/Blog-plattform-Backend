from django.db import models
from base.models import BaseModel
from django_ckeditor_5.fields import CKEditor5Field 

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Blog(BaseModel):
    STATUS_CHOICES  = (
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
    

