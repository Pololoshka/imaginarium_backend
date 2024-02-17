import random

from django.db import models
from django.db.models.query import QuerySet

from game.models.color import Color
from game.models.pawn import Pawn

# class RoomQuerySet(models.QuerySet):
#     ...


class RoomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def create_(self, number_of_pawns: int) -> "Room":
        while True:
            code = "".join([str(i) for i in random.choices(range(10), k=6)])
            if not self.get_queryset().filter(code=code).exists():
                room = self.create(code=code, number_of_pawns=number_of_pawns)
                break
        for color in Color.objects.all()[:number_of_pawns]:
            Pawn.objects.create(color=color, room=room)
        return room


class Room(models.Model):
    code = models.CharField(unique=True, max_length=6, primary_key=True)
    number_of_pawns = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    custom_objects = RoomManager()
