from django.db import models


class PawnVote(models.Model):
    pawn = models.ForeignKey("Pawn", on_delete=models.CASCADE, related_name="vote")
    room_card = models.ForeignKey("RoomCard", on_delete=models.CASCADE, related_name="pawn_votes")

    objects = models.Manager()

    class Meta:
        db_table = "pawn_votes"
