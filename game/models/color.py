from django.db import models


class Color(models.Model):
    name = models.CharField(unique=True, primary_key=True)

    objects = models.Manager()

    class Meta:
        db_table = "colors"

    def __str__(self) -> str:
        return self.name
