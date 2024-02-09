from rest_framework import serializers

from game.models.pawn import Pawn


class PawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pawn
        fields = ("player", "color", "is_ready", "score")
