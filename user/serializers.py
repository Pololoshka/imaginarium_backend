from django.contrib.auth.models import User
from rest_framework import serializers

from game.serializers import PlayerSerializer


class UserSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "player",
        )
