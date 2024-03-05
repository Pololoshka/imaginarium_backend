from typing import Any

from django.db.models import QuerySet
from pydantic import BaseModel, ConfigDict, Field, field_validator

from game import models as m
from game.models_pydantic.pawn import Pawn


class Room(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str = Field(max_length=6, min_length=6)
    pawns: list[Pawn]

    @field_validator("pawns", mode="before")
    @classmethod
    def _from_queryset(cls, v: Any) -> QuerySet[m.Pawn]:
        return v.all()  # type: ignore
