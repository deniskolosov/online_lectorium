from django.db import models
from afi_backend.users.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
