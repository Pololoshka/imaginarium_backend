from django.contrib import admin

from game.models.color import Color
from game.models.room import Room

admin.site.register(Room)
admin.site.register(Color)
