from rest_framework import permissions, viewsets
from rest_framework.response import Response

from . import models as m
from . import serializers as s


class RoomViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = m.Room.objects.all()
    serializer_class = s.RoomSerializer
    # authentication_classes = [AuthenticationBySession]

    def list(self, request):
        queryset = m.Room.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
