from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pydantic import BaseModel, Field, validate_call

from game.exceptions import GameError
from game.models.pawn import Pawn


class RequestData(BaseModel):
    pawn_id: int | None
    room_code: str = Field(min_length=6, max_length=6)


@validate_call(config={"arbitrary_types_allowed": True})
def handle_chooese_pawn(data: RequestData, user: User) -> None:
    try:
        prev_pawn = user.player.pawn
        prev_pawn.player = None
        prev_pawn.save()
    except ObjectDoesNotExist:
        ...
    if data.pawn_id is None:
        return
    new_pawn = Pawn.objects.get(id=data.pawn_id, room_id=data.room_code)
    if new_pawn.player is not None:
        raise GameError("Pawn is not free")

    new_pawn.player = user.player
    new_pawn.save()
