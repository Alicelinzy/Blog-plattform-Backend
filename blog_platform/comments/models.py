from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from blog.models import Blog
from accounts.models import Author, Reader
from base.models import BaseModel
from accounts.models import User

class Comment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_comments")  
    reader = models.ForeignKey(Reader, on_delete=models.SET_NULL, null=True, blank=True, related_name="reader_comments")  
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies") 
    content = CKEditor5Field(config_name="default")  
    is_approved = models.BooleanField(default=True)
    user_role = models.CharField(max_length=10, choices=[("author", "Author"), ("reader", "Reader")], blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Automatically set user_role based on whether the user is an Author or Reader """
        if hasattr(self.user, "author"):
            self.user_role = "author"
            self.author = self.user.author  
        elif hasattr(self.user, "reader"):
            self.user_role = "reader"
            self.reader = self.user.reader  
        else:
            self.user_role = None  
        super().save(*args, **kwargs)  

    def __str__(self):
        blog_title = self.blog.title if self.blog else "Unknown Blog"
        user_name = str(self.user) if self.user else "Anonymous"
        return f"{user_name} on {blog_title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
