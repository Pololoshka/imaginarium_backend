from django.contrib import admin

from game.models import Card, Color, Room

admin.site.register(Room)
admin.site.register(Color)
admin.site.register(Card)
