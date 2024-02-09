import random
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from game.models.color import Color
from game.models.pawn import Pawn

from game.models.room import Room
from game.serializers.room import RoomCreateSerializer, RoomGetSerializer, RoomSerializer




class RoomViewset(viewsets.ViewSet):
    # queryset = Room.objects.all()

    def retrieve(self, request: Request, pk:str) -> Response:
        room=get_object_or_404(Room, pk=pk)
        return Response(RoomSerializer(room).data)

    def create(self, request: Request) -> Response:
        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room=Room.custom_objects.create_(number_of_pawns=serializer.validated_data["number_of_pawns"])

        return Response(RoomSerializer(room).data)
