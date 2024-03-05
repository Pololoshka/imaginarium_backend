from rest_framework import serializers

from game.models import Player
from game.models.pawn import Pawn
from game.serializers.color import ColorSerializer


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "user")


class PawnPlayerSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = Pawn
        fields = (
            "id",
            "room",
            "color",
            "is_lead",
            "score",
        )


class PlayerUserSerializer(serializers.ModelSerializer):
    pawn = PawnPlayerSerializer()

    class Meta:
        model = Player
        fields = ("name", "user", "pawn")
