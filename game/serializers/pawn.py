from rest_framework import serializers

from game.models.pawn import Pawn
from game.serializers.player import PlayerSerializer


class PawnSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = Pawn
        fields = (
            "player",
            "color",
            "is_ready",
            "score",
        )
