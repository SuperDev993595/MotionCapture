from typing_extensions import Optional

from models.custom_base_model import CustomBaseModel
from models.move_type import MoveType


class Move(CustomBaseModel):
    move_type: MoveType
    x: Optional[int] = None
    y: Optional[int] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    button_name: Optional[str] = None
    key_code: Optional[str] = None
    key_name: Optional[str] = None
