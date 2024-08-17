from enum import Enum


class LogLevel(Enum):
    DISABLED = (0, 'disabled')
    ERROR = (1, 'error')
    WARNING = (2, 'warning')
    INFO = (3, 'info')
    DEBUG = (4, 'debug')

    def __str__(self):
        return self.value[1]

    def get_value(self):
        return self.value[0]

    @classmethod
    def from_string(cls, s: str) -> 'LogLevel':
        for log_value in cls:
            if log_value.value[1] == s:
                return log_value
        raise ValueError(cls.__name__ + ' has no value matching "' + s + '"')

    @classmethod
    def from_value(cls, v: int) -> 'LogLevel':
        for log_value in cls:
            if log_value.value[0] == v:
                return log_value
        raise ValueError(cls.__name__ + ' has no value matching "' + str(v) + '"')
