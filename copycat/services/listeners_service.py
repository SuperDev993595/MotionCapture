from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

from copycat.shared.utils.logger import Logger
from models.history import History
from models.move import Move
from models.move_type import MoveType


class ListenersService:

    def __init__(self):
        self.logger = Logger()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.history: History = History()
        self.create_listeners()

    def create_listeners(self) -> None:
        self.mouse_listener = MouseListener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)

    def get_history(self) -> History:
        return self.history

    def clean_history(self) -> None:
        self.history = []

    def start_listeners(self) -> None:
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listener(self) -> None:
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.logger.info("Listeners stopped")

    def on_click(self, x, y, button, pressed) -> None:
        if pressed:
            self.logger.debug(f'Mouse clicked at ({x}, {y}) with {button} {pressed}')
            move = Move(move_type=MoveType.MOUSE_CLICK, x=x, y=y, button=button)
            self.history.add_move(move)

    def on_scroll(self, x, y, dx, dy) -> None:
        self.logger.debug(f'Mouse scrolled at ({x}, {y})({dx}, {dy})')
        move = Move(move_type=MoveType.MOUSE_SCROLL, x=x, y=y, dx=dx, dy=dy)
        self.history.add_move(move)

    def on_press(self, key) -> None:
        self.logger.debug(f"Key pressed: {key}")
        if key == keyboard.Key.esc:
            self.logger.debug("Stopping listeners")
            self.stop_listener()
        move = Move(move_type=MoveType.KEY_PRESS, key=key)
        self.history.add_move(move)

    def on_move(self, x, y) -> None:
        self.logger.debug(f"Mouse moved to ({x}, {y})")
        move = Move(move_type=MoveType.MOUSE_MOVE, x=x, y=y)
        self.history.add_move(move)
