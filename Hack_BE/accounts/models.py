from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

  #email = None
  REQUIRED_FIELDS = []
  
  nickname = models.CharField(max_length=100)
  age = models.CharField(max_length=20)
  location = models.CharField(max_length=200)

  def __str__(self):
        return self.nickname