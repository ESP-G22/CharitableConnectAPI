from django.db import models
import uuid

class Image(models.Model):
    file = models.ImageField(upload_to='static/images')
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.id

