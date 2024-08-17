import time

import pyautogui
from pynput.keyboard import Controller as KeyboardController, KeyCode, Key
from pynput.mouse import Controller as MouseController, Button

from copycat.models.history.history import History
from copycat.models.move.move import Move
from copycat.models.move.move_type import MoveType
from copycat.shared.utils.logger import Logger


class PlaybackService:
    # TODO: Add a setting to enable/disable native input
    use_native_input = True

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
            button = self.get_button(move)
            if move.pressed:
                self.mouse_controller.press(button)
            else:
                self.mouse_controller.release(button)
        elif move.move_type == MoveType.MOUSE_SCROLL:
            self.mouse_controller.scroll(move.dx, move.dy)
        elif move.move_type == MoveType.MOUSE_MOVE:
            self.mouse_controller.position = (move.x, move.y)
        elif move.move_type == MoveType.KEY_PRESS:
            self.press_key(move)
        elif move.move_type == MoveType.KEY_RELEASED:
            self.release_key(move)
        else:
            self.logger.error(f"Unknown move type: {move.move_type}")

    def press_key(self, move: Move) -> None:
        if self.use_native_input:
            key = self.get_key_name(move)
            pyautogui.keyDown(key, _pause=False)
        else:
            key = self.get_key(move)
            self.keyboard_controller.press(key)

    def release_key(self, move: Move) -> None:
        if self.use_native_input:
            key = self.get_key_name(move)
            pyautogui.keyUp(key, _pause=False)
        else:
            key = self.get_key(move)
            self.keyboard_controller.release(key)

    @staticmethod
    def get_key(move: Move) -> Key | KeyCode:
        if move.key_code:
            return KeyCode.from_char(move.key_code)
        elif move.key_name:
            return getattr(Key, move.key_name)

    @staticmethod
    def get_key_name(move: Move) -> str:
        if move.key_code:
            return move.key_code
        elif move.key_name:
            return move.key_name

    @staticmethod
    def get_button(move: Move) -> Button:
        return getattr(Button, move.button_name)
