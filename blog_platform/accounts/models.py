from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

class AuthorManager(models.Manager):
    def active_authors(self):
        return self.filter(user__is_active=True)

class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Adding the custom manager
    objects = AuthorManager()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.user.username} (Author)"


class Reader(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader")
    favorite_categories = models.ManyToManyField("blog.Category", blank=True) 

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def __str__(self):
        return f"{self.user.username} (Reader)"
