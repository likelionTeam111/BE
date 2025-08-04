from django.db import models

# Create your models here.

class Policy(models.Model):
    plcyNo = models.CharField(max_length=100,unique=True)
    plcyNm = models.