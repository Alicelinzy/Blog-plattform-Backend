from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel


class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.username} (Author)"


class Reader(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader")
    favorite_categories = models.ManyToManyField("blog.Category", blank=True) 

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def __str__(self):
        return f"{self.username} (Reader)"

