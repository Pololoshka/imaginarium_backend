import random

from django.db import models
from django.db.models.query import QuerySet

from game.models import Card, Color, Pawn
from game.models.room_card import RoomCard


class RoomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def create_(self, number_of_pawns: int) -> "Room":
        while True:
            code = "".join([str(i) for i in random.choices(range(10), k=6)])
            if not self.get_queryset().filter(code=code).exists():
                room: Room = self.create(code=code)  # type: ignore
                break

        for color in Color.objects.all()[:number_of_pawns]:
            Pawn.objects.create(color=color, room=room)
        for card in Card.objects.order_by("?").all():
            RoomCard.objects.create(room=room, card=card)
        self.identify_lead(room=room)
        self.deal_cards(room=room, number_of_pawns=number_of_pawns)
        return room

    def deal_cards(self, room: "Room", number_of_pawns: int) -> None:
        room_cards = list(
            RoomCard.objects.filter(room=room).order_by("id")[: (number_of_pawns * 6)]
        )
        pawns = list(Pawn.objects.filter(room=room).all())
        count = 0

        for index in range(1, number_of_pawns * 6 + 1):
            room_cards[index - 1].pawn = pawns[count]
            room_cards[index - 1].save()
            if index % 6 == 0:
                count += 1

    def identify_lead(self, room: "Room") -> None:
        if first_pawn := Pawn.objects.filter(room=room).first():
            first_pawn.is_lead = True
            first_pawn.save()


class Room(models.Model):
    code = models.CharField(unique=True, max_length=6, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    custom_objects = RoomManager()

    class Meta:
        db_table = "rooms"
