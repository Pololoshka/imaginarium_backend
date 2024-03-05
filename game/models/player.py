from django.contrib.auth.models import User
from django.db import models


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player")
    name = models.CharField(max_length=20, default="Anonymous")

    objects = models.Manager()

    class Meta:
        db_table = "players"
