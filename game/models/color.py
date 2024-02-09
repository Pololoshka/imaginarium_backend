from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)

    objects = models.Manager()

    def __str__(self) -> str:
        return self.name
