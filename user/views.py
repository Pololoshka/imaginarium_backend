import uuid

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Player


class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes: list = []

    def post(self, _request: Request) -> Response:
        user = User.objects.create(username=uuid.uuid4())
        token = Token.objects.create(user=user)
        Player.objects.create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )
