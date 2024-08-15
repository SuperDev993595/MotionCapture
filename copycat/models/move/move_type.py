from enum import Enum


class MoveType(str, Enum):
    MOUSE_CLICK = 'MOUSE_CLICK'
    MOUSE_SCROLL = 'MOUSE_SCROLL'
    MOUSE_MOVE = 'MOUSE_MOVE'
    KEY_PRESS = 'KEY_PRESS'
    KEY_RELEASED = 'KEY_RELEASED'
