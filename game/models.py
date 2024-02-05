from django.db import models

# Create your models here.


class Room(models.Model):
    code = models.CharField(unique=True, max_length=10)
