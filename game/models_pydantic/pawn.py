from typing import Any

from django.db.models import QuerySet
from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from game import models as m
from game.models_pydantic.room_card import RoomCard

from .player import Player


class Pawn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player: Player | None
    color: str = Field(validation_alias=AliasPath("color", "name"))
    is_lead: bool
    score: int
    room_card: list[RoomCard] = []

    @field_validator("room_card", mode="before")
    @classmethod
    def _from_queryset(cls, v: Any) -> QuerySet[m.RoomCard]:
        return v.all()  # type: ignore
