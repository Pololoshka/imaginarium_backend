from django.contrib.auth.models import User
from pydantic import BaseModel, validate_call

from game.models.room_card import RoomCard


class RequestData(BaseModel):
    association: str
    card: int


@validate_call(config={"arbitrary_types_allowed": True})
def handle_come_up_with_an_association(data: RequestData, user: User) -> None:
    room_card = RoomCard.objects.get(id=data.card)
    room_card.is_active = True
    room_card.association = data.association
    room_card.save()
