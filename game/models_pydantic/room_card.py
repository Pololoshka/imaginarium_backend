from pydantic import AliasPath, BaseModel, ConfigDict, Field


class RoomCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    card: int = Field(validation_alias=AliasPath("card", "id"))
    is_active: bool
    association: str | None
