from django.db import models
from django.db.models.query import QuerySet



# class PawnManager(models.Manager):
#     def get_queryset(self) -> QuerySet:
#         return super().get_queryset()


class Pawn(models.Model):
    player = models.OneToOneField("Player", on_delete=models.CASCADE, null=True)
    color = models.ForeignKey("Color", on_delete=models.CASCADE, to_field="name")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="pawns")
    is_ready = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0)

    objects = models.Manager()
    # custom_objects = PawnManager()
