from rest_framework import serializers

from game.models.room import Room
from game.serializers.pawn import PawnSerializer


class RoomCreateSerializer(serializers.ModelSerializer):
    number_of_pawns = serializers.IntegerField(min_value=4, max_value=4)

    class Meta:
        model = Room
        fields = ("number_of_pawns",)


class RoomSerializer(serializers.ModelSerializer):
    pawns = PawnSerializer(many=True)

    class Meta:
        model = Room
        fields = (
            "code",
            "number_of_pawns",
            "pawns",
        )

    depth = 4
