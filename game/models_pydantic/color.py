from pydantic import BaseModel, ConfigDict


class Color(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
