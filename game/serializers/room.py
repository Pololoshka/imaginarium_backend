from rest_framework import serializers

from game.models.room import Room
from game.serializers.pawn import PawnSerializer


class RoomCreateSerializer(serializers.Serializer):
    number_of_pawns = serializers.IntegerField(min_value=4, max_value=4)


class RoomSerializer(serializers.ModelSerializer):
    pawns = PawnSerializer(many=True)

    class Meta:
        model = Room
        fields = (
            "code",
            "pawns",
        )

    depth = 5
