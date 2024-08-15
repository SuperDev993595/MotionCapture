import time

from pynput.keyboard import Controller as KeyboardController, KeyCode, Key
from pynput.mouse import Controller as MouseController, Button

from copycat.shared.utils.logger import Logger
from models.history.history import History
from models.move.move import Move
from models.move.move_type import MoveType


class PlaybackService:

    def __init__(self):
        self.logger = Logger()
        self.mouse_controller = None
        self.keyboard_controller = None
        self.create_controllers()

    def create_controllers(self) -> None:
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()

    def play(self, history: History) -> None:
        for move in history.moves:
            time.sleep(move.delay)
            self.play_move(move)

    def play_move(self, move: Move) -> None:
        if move.move_type == MoveType.MOUSE_CLICK:
            self.mouse_controller.position = (move.x, move.y)
            button = getattr(Button, move.button_name)
            self.mouse_controller.press(button)
            self.mouse_controller.release(button)
        elif move.move_type == MoveType.MOUSE_SCROLL:
            self.mouse_controller.scroll(move.dx, move.dy)
        elif move.move_type == MoveType.MOUSE_MOVE:
            self.mouse_controller.position = (move.x, move.y)
        elif move.move_type == MoveType.KEY_PRESS:
            key = self.get_key(move)
            self.keyboard_controller.press(key)
        elif move.move_type == MoveType.KEY_RELEASED:
            key = self.get_key(move)
            self.keyboard_controller.release(key)
        else:
            self.logger.error(f"Unknown move type: {move.move_type}")

    @staticmethod
    def get_key(move: Move):
        if move.key_code:
            return KeyCode.from_char(move.key_code)
        elif move.key_name:
            return getattr(Key, move.key_name)
