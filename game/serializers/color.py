from rest_framework import serializers

from game.models.color import Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name",)
