from django.db import models


class RoomCard(models.Model):
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="cards")
    pawn = models.ForeignKey("Pawn", on_delete=models.CASCADE, related_name="room_cards", null=True)
    card = models.ForeignKey("Card", on_delete=models.CASCADE, related_name="room")
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    association = models.CharField(max_length=200, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "room_cards"
        constraints = [
            models.UniqueConstraint(
                fields=["pawn"],
                condition=models.Q(is_active=True),
                name="unique_active_card_pawn",
            )
        ]
