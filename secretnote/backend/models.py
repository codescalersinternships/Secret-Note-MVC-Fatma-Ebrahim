from django.db import models
import uuid 
# Create your models here.
class Note(models.Model):
    def __str__(self):
        return self.content
 
    content=models.TextField()
    url=models.UUIDField(unique=True,max_length=8,default=uuid.uuid4, editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    expiration=models.DateTimeField()
    views_limit=models.PositiveIntegerField(default=10)
    