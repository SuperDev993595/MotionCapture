from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode
from pynput.mouse import Listener as MouseListener, Button
from copycat.models.history.history import History
from copycat.models.move.move import Move
from copycat.models.move.move_type import MoveType
from copycat.shared.utils.generic import get_timestamp
from copycat.shared.utils.logger import Logger


class ListenersService:
    POOLING_INTERVAL: float = 0.03  # Renamed for clarity and consistency
    EXIT_KEY: Key = Key.esc  # Renamed for clarity and consistency

    def __init__(self):
        self.logger = Logger()
        self.mouse_listener: MouseListener | None = None
        self.keyboard_listener: KeyboardListener | None = None
        self.history: History = History()
        self.last_mouse_move_time: float = get_timestamp()

    def create_listeners(self) -> None:
        """Initialize mouse and keyboard listeners."""
        self.mouse_listener = MouseListener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move
        )
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def get_history(self) -> History:
        """Return the recorded history."""
        return self.history

    def clean_history(self) -> None:
        """Reset the history."""
        self.history = History()

    def start_recording(self) -> None:
        """Start recording user actions."""
        self.history.start()
        self.start_listeners()

    def stop_recording(self) -> None:
        """Stop recording user actions."""
        self.history.stop()
        self.stop_listeners()

    def start_listeners(self) -> None:
        """Start mouse and keyboard listeners."""
        self.create_listeners()
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listeners(self) -> None:
        """Stop mouse and keyboard listeners."""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.logger.info("Listeners stopped")

    def on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Handle mouse click events."""
        self.logger.debug(f'Mouse clicked at ({x}, {y}) with {button} {pressed}')
        move = Move(
            move_type=MoveType.MOUSE_CLICK,
            x=x,
            y=y,
            button_name=button.name,
            pressed=pressed
        )
        self.add_move(move)

    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle mouse scroll events."""
        self.logger.debug(f'Mouse scrolled at ({x}, {y})({dx}, {dy})')
        move = Move(
            move_type=MoveType.MOUSE_SCROLL,
            x=x,
            y=y,
            dx=dx,
            dy=dy
        )
        self.add_move(move)

    def on_press(self, key: Key | KeyCode) -> None:
        """Handle key press events."""
        self.logger.debug(f"Key pressed: {key}")
        if key == self.EXIT_KEY:
            self.logger.info("Ignoring Exit Key On Press")
            return
        key_code, key_name = self.get_key(key)
        move = Move(
            move_type=MoveType.KEY_PRESS,
            key_code=key_code,
            key_name=key_name
        )
        self.add_move(move)

    def on_release(self, key: Key | KeyCode) -> None:
        """Handle key release events."""
        self.logger.debug(f"Key released: {key}")
        if key == self.EXIT_KEY:
            self.logger.info("Ignoring Exit Key On Release")
            return
        key_code, key_name = self.get_key(key)
        move = Move(
            move_type=MoveType.KEY_RELEASED,
            key_code=key_code,
            key_name=key_name
        )
        self.add_move(move)

    def on_move(self, x: int, y: int) -> None:
        """Handle mouse move events."""
        self.logger.debug(f"Mouse moved to ({x}, {y})")
        now = get_timestamp()
        time_diff = now - self.last_mouse_move_time
        if time_diff > self.POOLING_INTERVAL:
            self.logger.debug("Mouse move saved to history")
            self.last_mouse_move_time = now
            move = Move(
                move_type=MoveType.MOUSE_MOVE,
                x=x,
                y=y
            )
            self.add_move(move)

    def add_move(self, move: Move) -> None:
        """Add a move to the history."""
        self.history.add_move(move)

    @staticmethod
    def get_key(key: Key | KeyCode) -> tuple[str | None, str | None]:
        """Extract key code and name from a key event."""
        key_code = None
        key_name = None
        if isinstance(key, KeyCode):
            key_code = key.char
        elif isinstance(key, Key):
            key_name = key.name
        return key_code, key_name


def save_history_to_file(self, file_path: str, format: str = 'json') -> None:
    """
    Save the recorded history to a file.

    :param file_path: Path to the output file.
    :param format: File format ('json' or 'csv').
    """
    if format == 'json':
        with open(file_path, 'w') as file:
            json.dump([move.to_dict() for move in self.history.get_moves()], file, indent=4)
    elif format == 'csv':
        import csv
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'X', 'Y', 'Button', 'Pressed', 'Key Code', 'Key Name', 'DX', 'DY'])
            for move in self.history.get_moves():
                writer.writerow([
                    move.move_type.value,
                    move.x,
                    move.y,
                    move.button_name,
                    move.pressed,
                    move.key_code,
                    move.key_name,
                    move.dx,
                    move.dy
                ])
    else:
        raise ValueError("Unsupported format. Use 'json' or 'csv'.")
    self.logger.info(f"History saved to {file_path} in {format} format.")        


    def clear_moves_by_type(self, move_type: MoveType) -> None:
    """
    Remove moves of a specific type from the history.

    :param move_type: The type of move to remove (e.g., MoveType.MOUSE_CLICK).
    """
    self.history.moves = [move for move in self.history.get_moves() if move.move_type != move_type]
    self.logger.info(f"All {move_type.value} moves cleared from history.")