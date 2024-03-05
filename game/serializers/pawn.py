from typing import TYPE_CHECKING

from rest_framework import serializers

from game.models.color import Color
from game.models.pawn import Pawn
from game.serializers.player import PlayerSerializer
from game.serializers.room_card import RoomCardSerializer

if TYPE_CHECKING:
    from rest_framework.relations import RelatedField


class PawnSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    color: "RelatedField[Color, str, str]" = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
    room_card = RoomCardSerializer(many=True)

    class Meta:
        model = Pawn
        fields = (
            "id",
            "player",
            "color",
            "is_lead",
            "score",
            "room_card",
        )
