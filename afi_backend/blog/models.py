from django.db import models
from afi_backend.users.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from afi_backend.events.models import Category


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    picture = models.ImageField(upload_to='blog_pictures/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.author}: {self.description[10:]}"
