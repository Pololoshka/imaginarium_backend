from typing import TYPE_CHECKING

from rest_framework import serializers

from game.models import RoomCard

if TYPE_CHECKING:
    from rest_framework.relations import RelatedField


class RoomCardSerializer(serializers.ModelSerializer):
    card: "RelatedField[RoomCard, str, str]" = serializers.SlugRelatedField(
        slug_field="id", read_only=True
    )

    class Meta:
        model = RoomCard
        fields = (
            "id",
            "card",
            "is_active",
            "association",
        )
