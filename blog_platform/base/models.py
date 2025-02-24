from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()  

class BaseModel(models.Model):
    created_at = models.DateTimeField(default = now) 
    updated_at = models.DateTimeField(auto_now=True)  
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
    related_name="created_%(class)s"
    )  
    updated_by = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, 
    related_name="updated_%(class)s"
    )  

    class Meta:
        abstract = True  
