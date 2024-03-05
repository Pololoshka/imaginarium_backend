from django.db import models


class Card(models.Model):
    id = models.PositiveSmallIntegerField(unique=True, primary_key=True)

    objects = models.Manager()

    class Meta:
        db_table = "cards"

    def __str__(self) -> str:
        return str(self.id)
