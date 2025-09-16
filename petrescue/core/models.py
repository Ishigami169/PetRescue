from django.db import models

# Create your models here.
# In core/models.py
from django.conf import settings

class BaseModel(models.Model):
    """
    An abstract base model that provides common fields for tracking
    creation and modification details.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Allow creating objects without a user (e.g., in scripts)
        related_name='%(app_label)s_%(class)s_created_by'
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Allow modifying objects without a user
        related_name='%(app_label)s_%(class)s_modified_by'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        # This tells Django that this model is abstract and should not
        # be used to create a database table.
        abstract = True