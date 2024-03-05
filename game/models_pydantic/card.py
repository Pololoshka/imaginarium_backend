from pydantic import BaseModel, ConfigDict


class Card(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
