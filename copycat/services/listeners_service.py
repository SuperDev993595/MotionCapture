from datetime import datetime, timedelta

from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode
from pynput.mouse import Listener as MouseListener, Button

from copycat.shared.utils.logger import Logger
from models.history.history import History
from models.move.move import Move
from models.move.move_type import MoveType


class ListenersService:
    pooling: int = 100_000
    exit_key: Key = Key.esc

    def __init__(self):
        self.logger = Logger()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.history: History = History()
        self.last_mouse_move_time: datetime = datetime.now()

    def create_listeners(self) -> None:
        self.mouse_listener = MouseListener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)

    def get_history(self) -> History:
        return self.history

    def clean_history(self) -> None:
        self.history = History()

    def start_recording(self) -> None:
        self.history.start()
        self.start_listeners()

    def stop_recording(self) -> None:
        self.history.stop()
        self.stop_listener()

    def start_listeners(self) -> None:
        self.create_listeners()
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listener(self) -> None:
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.logger.info("Listeners stopped")

    def on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        if pressed:
            self.logger.debug(f'Mouse clicked at ({x}, {y}) with {button} {pressed}')
            move = Move(move_type=MoveType.MOUSE_CLICK, x=x, y=y, button_name=button.name)
            self.history.add_move(move)

    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        self.logger.debug(f'Mouse scrolled at ({x}, {y})({dx}, {dy})')
        move = Move(move_type=MoveType.MOUSE_SCROLL, x=x, y=y, dx=dx, dy=dy)
        self.history.add_move(move)

    def on_press(self, key: Key | KeyCode) -> None:
        self.logger.debug(f"Key pressed: {key}")
        key_code, key_name = self.get_key(key)
        move = Move(move_type=MoveType.KEY_PRESS, key_code=key_code, key_name=key_name)
        self.history.add_move(move)

    def on_release(self, key: Key | KeyCode) -> None:
        self.logger.debug(f"Key released: {key}")
        if key == self.exit_key:
            self.logger.debug("Stopping listeners")
            self.stop_listener()
        key_code, key_name = self.get_key(key)
        move = Move(move_type=MoveType.KEY_RELEASED, key_code=key_code, key_name=key_name)
        self.history.add_move(move)

    def on_move(self, x: int, y: int) -> None:
        self.logger.debug(f"Mouse moved to ({x}, {y})")
        now = datetime.now()
        time_diff = now - self.last_mouse_move_time
        if time_diff.microseconds > self.pooling:
            self.logger.debug(f"Mouse move saved to history")
            self.last_mouse_move_time = datetime.now() + timedelta(milliseconds=self.pooling)
            move = Move(move_type=MoveType.MOUSE_MOVE, x=x, y=y)
            self.history.add_move(move)

    @staticmethod
    def get_key(key: Key | KeyCode) -> tuple[str, str]:
        key_code = None
        key_name = None
        if isinstance(key, KeyCode):
            key_code = key.char
        elif isinstance(key, Key):
            key_name = key.name
        return key_code, key_name
