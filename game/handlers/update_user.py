from django.contrib.auth.models import User
from pydantic import BaseModel, validate_call


class RequestData(BaseModel):
    player_name: str


@validate_call(config={"arbitrary_types_allowed": True})
def handle_user_update(data: RequestData, user: User) -> None:
    user.player.name = data.player_name
    user.player.save()
