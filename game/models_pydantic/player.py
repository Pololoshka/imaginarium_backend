from pydantic import AliasPath, BaseModel, ConfigDict, Field


class Player(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: int = Field(validation_alias=AliasPath("user", "id"))
    name: str
