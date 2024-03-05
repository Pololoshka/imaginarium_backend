from django.contrib.auth.models import User
from rest_framework import serializers

from game.serializers.player import PlayerUserSerializer


class UserSerializer(serializers.ModelSerializer):
    player = PlayerUserSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "player",
        )
