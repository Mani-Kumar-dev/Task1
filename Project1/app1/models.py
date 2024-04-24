from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Request_user(models.Model):
    user_Id=models.ForeignKey(User,on_delete=models.CASCADE)
    requesttype=models.CharField(max_length=256)
    reason=models.CharField(max_length=256)
    status=models.CharField(max_length=256)
    