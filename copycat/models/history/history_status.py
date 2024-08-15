from enum import Enum


class HistoryStatus(str, Enum):
    STOPPED = 'STOPPED'
    STARTED = 'STARTED'
