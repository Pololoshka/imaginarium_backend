from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pydantic import BaseModel, Field, validate_call


class RequestData(BaseModel):
    room_code: str = Field(min_length=6, max_length=6)


@validate_call(config={"arbitrary_types_allowed": True})
def handle_leave_room(data: RequestData, user: User) -> None:
    try:
        prev_pawn = user.player.pawn
        prev_pawn.player = None
        prev_pawn.save()
    except ObjectDoesNotExist:
        ...
