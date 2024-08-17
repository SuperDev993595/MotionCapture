from typing import List, Optional

from copycat.models.custom_base_model import CustomBaseModel
from copycat.models.history.history_status import HistoryStatus
from copycat.models.move.move import Move
from copycat.shared.utils.generic import get_timestamp


class History(CustomBaseModel):
    moves: List[Move] = []
    last_move_time: Optional[float] = None
    status: HistoryStatus = HistoryStatus.STOPPED

    def start(self) -> None:
        self.last_move_time = get_timestamp()
        self.status = HistoryStatus.STARTED

    def stop(self) -> None:
        self.status = HistoryStatus.STOPPED
        self.last_move_time = get_timestamp()

    def add_move(self, move: Move) -> None:
        if self.status == HistoryStatus.STOPPED:
            return
        delay = get_timestamp() - self.last_move_time
        self.last_move_time += delay
        move.set_delay(delay)
        self.moves.append(move)
