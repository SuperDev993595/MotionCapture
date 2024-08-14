from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        underscore_attrs_are_private = True
