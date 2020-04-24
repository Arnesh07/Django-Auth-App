from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)