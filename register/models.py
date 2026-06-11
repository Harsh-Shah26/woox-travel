from django.db import models
from django.contrib.auth.models import AbstractUser

class Register(models.Model):
    username = models.CharField(max_length=10)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    
# class UserType(AbstractUser):
#     is_admin = models.BooleanField('Is admin',default=False)
#     is_user = models.BooleanField('Is user',default=False)

# Create your models here.
