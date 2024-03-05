from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from game.models.pawn import Pawn
from game.models.room import Room
from game.models.room_card import RoomCard
from game.serializers.room import RoomCreateSerializer, RoomSerializer


class RoomViewset(viewsets.ViewSet):
    def retrieve(self, request: Request, pk: str) -> Response:
        room = (
            Room.objects.prefetch_related(Prefetch("pawns", queryset=Pawn.objects.order_by("id")))
            .prefetch_related("pawns__color")
            .prefetch_related("pawns__player")
            .prefetch_related("pawns__player__user")
            .prefetch_related(
                Prefetch(
                    "pawns__room_card",
                    queryset=RoomCard.objects.filter(is_deleted=False).order_by("id"),
                )
            )
            .prefetch_related("pawns__room_card__card")
            .get(pk=pk)
        )

        return Response(RoomSerializer(room).data)

    def create(self, request: Request) -> Response:
        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = Room.custom_objects.create_(
            number_of_pawns=serializer.validated_data["number_of_pawns"]
        )
        return Response(RoomSerializer(room).data)
