from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # Short biography
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="author_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="author_permissions",
        blank=True
    )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.username} (Author)"


class Reader(AbstractUser):
    favorite_categories = models.ManyToManyField("blog.Category", blank=True)  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="reader_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="reader_permissions",
        blank=True
    )

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def __str__(self):
        return f"{self.username} (Reader)"

