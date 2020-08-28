from django.db import models
import uuid
from afi_backend.users import models as user_models

# Create your models here.

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user =  models.ForeignKey(user_models.User, on_delete=models.CASCADE)
