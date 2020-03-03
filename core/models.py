"""Core models."""

from django.core.validators import FileExtensionValidator
from django.db import models


class FileUpload(models.Model):
    file = models.FileField(upload_to='file', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    filename = models.CharField(max_length=1024)

    def __str__(self):
        return self.filename
