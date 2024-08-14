from typing import List

from models.custom_base_model import CustomBaseModel
from models.move import Move


class History(CustomBaseModel):
    moves: List[Move] = []

    def add_move(self, move: Move) -> None:
        self.moves.append(move)
