from datetime import datetime
from typing import List, Optional

from models.custom_base_model import CustomBaseModel
from models.history.history_status import HistoryStatus
from models.move.move import Move


class History(CustomBaseModel):
    moves: List[Move] = []
    last_move_time: Optional[datetime] = None
    status: HistoryStatus = HistoryStatus.STOPPED

    def start(self) -> None:
        self.last_move_time = datetime.now()
        self.status = HistoryStatus.STARTED

    def stop(self) -> None:
        self.status = HistoryStatus.STOPPED
        self.last_move_time = datetime.now()

    def add_move(self, move: Move) -> None:
        if self.status == HistoryStatus.STOPPED:
            return
        now = datetime.now()
        delay = (now - self.last_move_time).total_seconds()
        self.last_move_time = now
        move.set_delay(delay)
        self.moves.append(move)
