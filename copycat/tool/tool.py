import threading
import tkinter as tk
from textwrap import dedent
from tkinter import ttk
from typing import Callable, List

from pynput.keyboard import Listener as KeyboardListener
from ttkthemes.themed_tk import ThemedTk

from copycat.services.listeners_service import ListenersService
from copycat.services.playback_service import PlaybackService
from copycat.services.storage_service import StorageService
from copycat.shared.utils.logger import Logger

DESCRIPTION = dedent("""
Copycat is a simple macro recorder and player tool.
It allows you to record your keyboard and mouse inputs and play them back.
No tutorial needed, just start record, save and play it back.
Just a single tip: ESC key pause the recording.

More information can be found at https://github.com/ZappaBoy/copycat
Feel free to contribute to the project, open an issue or simply buy me a coffee.

Copycat was created by ZappaBoy. 
""")

DEFAULT_THEME: str = "equilux"
DEFAULT_SPEED: float = 1.0
NO_MACRO_SELECTED: str = "No macro selected"
DEFAULT_GEOMETRY_POPUP: str = "600x260"


class Tool:

    def __init__(self, theme: str = DEFAULT_THEME, speed: float = DEFAULT_SPEED):
        self.logger = Logger()
        self.width = 800
        self.height = 40
        self.geometry = f"{self.width}x{self.height}"
        self.window_title = "Copycat"
        self.theme = theme
        self.speed = speed
        self.root: tk.Tk | None = None
        self.logger.info("GUI initialized")
        self.listeners_service = ListenersService()
        self.playback_service = PlaybackService()
        self.storage_service = StorageService()
        self.save_window_popup: tk.Toplevel | None = None
        self.replay_window_popup: tk.Toplevel | None = None
        self.manage_window_popup: tk.Toplevel | None = None
        self.macro_name_input: tk.Entry | None = None
        self.speed_input: tk.Entry | None = None
        self.selected_macro_name: tk.StringVar | None = None
        self.available_macro_names: List[str] = []
        self.manage_macro_selector: tk.OptionMenu | None = None
        self.exit_key_listener = None
        self.stop_event: threading.Event | None = None

    def record(self):
        self.logger.info("Recording new macro")
        self.start_listeners()
        self.hide_window()

    def pause(self):
        self.logger.info("Pausing macro")
        self.stop_listeners()
        self.show_window()
        self.stop_event = None

    def save(self):
        self.logger.info("Saving macro")
        self.show_save_popup()
        self.listeners_service.stop_recording()
        self.listeners_service.clean_history()

    def discard(self):
        self.logger.info("Discarding macro")
        self.listeners_service.stop_recording()
        self.listeners_service.clean_history()

    def replay(self):
        self.logger.info("Replaying macro")
        self.show_replay_popup()

    def manage(self):
        self.logger.info("Managing macro")
        self.show_manage_popup()

    def show_info(self):
        self.logger.info("Showing info")
        self.show_info_popup()

    def close_window(self):
        self.logger.info("Closing window")
        self.root.destroy()

    def show(self):
        self.root = self.build_root()
        self.build_toolbar()
        self.root.mainloop()

    def build_root(self) -> tk.Tk:
        root = ThemedTk(theme=self.theme)
        root.title(self.window_title)
        root.geometry(self.geometry)
        root.resizable(False, False)
        return root

    def build_toolbar(self) -> tk.Frame:
        toolbar = tk.Frame()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.build_command_button(self.record, text="Record")
        self.build_command_button(self.pause, text="Pause")
        self.build_command_button(self.save, text="Save")
        self.build_command_button(self.discard, text="Discard")
        self.build_command_button(self.replay, text="Replay")
        self.build_command_button(self.manage, text="Manage")
        self.build_command_button(self.show_info, text="Info")
        self.build_command_button(self.close_window, text="Close")
        return toolbar

    @staticmethod
    def build_command_button(command: Callable, text: str = None) -> tk.Button:
        button = ttk.Button(text=text, command=command, width=10, padding=5)
        button.pack(side=tk.LEFT, expand=True)
        return button

    def build_popup(self, title: str, geometry: str = DEFAULT_GEOMETRY_POPUP) -> tk.Toplevel:
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(geometry)
        window.resizable(False, False)
        return window

    def show_save_popup(self):
        self.save_window_popup = self.build_popup("Save Macro")
        label = tk.Label(self.save_window_popup, text="Enter macro name:")
        label.pack()
        self.macro_name_input = tk.Entry(self.save_window_popup, width=30)
        self.macro_name_input.pack()
        save_button = ttk.Button(self.save_window_popup, text="Save", command=self.save_macro)
        save_button.pack(side=tk.LEFT, expand=True)
        close_button = ttk.Button(self.save_window_popup, text="Close", command=self.save_window_popup.destroy)
        close_button.pack(side=tk.LEFT, expand=True)
        self.save_window_popup.mainloop()

    def show_replay_popup(self):
        self.replay_window_popup = self.build_popup("Replay Macro")
        label = tk.Label(self.replay_window_popup, text="Enter macro name:")
        label.pack()
        self.update_available_macros()
        macro_selector = tk.OptionMenu(self.replay_window_popup, self.selected_macro_name,
                                       *self.available_macro_names)
        macro_selector.pack()
        label = tk.Label(self.replay_window_popup, text="Enter replay speed: (1.0 = real speed)")
        label.pack()
        self.speed_input = tk.Entry(self.replay_window_popup)
        self.speed_input.insert(0, str(self.speed))
        self.speed_input.pack()
        replay_button = ttk.Button(self.replay_window_popup, text="Replay", command=self.replay_macro)
        replay_button.pack(side=tk.LEFT, expand=True)
        close_button = ttk.Button(self.replay_window_popup, text="Close", command=self.replay_window_popup.destroy)
        close_button.pack(side=tk.LEFT, expand=True)
        self.replay_window_popup.mainloop()

    def show_manage_popup(self):
        self.manage_window_popup = self.build_popup("Manage Macros")
        label = tk.Label(self.manage_window_popup, text="Manage macros")
        label.pack()
        self.update_available_macros()
        self.manage_macro_selector = tk.OptionMenu(self.manage_window_popup, self.selected_macro_name,
                                                   *self.available_macro_names)
        self.manage_macro_selector.pack()
        delete_button = ttk.Button(self.manage_window_popup, text="Delete", command=self.delete_macro)
        delete_button.pack(side=tk.LEFT, expand=True)
        close_button = ttk.Button(self.manage_window_popup, text="Close", command=self.manage_window_popup.destroy)
        close_button.pack(side=tk.LEFT, expand=True)
        self.manage_window_popup.mainloop()

    def show_info_popup(self):
        window = self.build_popup("About Copycat")
        label = tk.Label(window, text=DESCRIPTION)
        label.pack()
        button = ttk.Button(window, text="Close", command=window.destroy)
        button.pack()
        window.mainloop()

    def save_macro(self):
        macro_name: str = self.macro_name_input.get()
        self.logger.debug(f"Saving macro {macro_name}")
        history = self.listeners_service.get_history()
        self.storage_service.save_history(macro_name=macro_name, data=history)
        self.save_window_popup.destroy()

    def replay_macro(self):
        macro_name = self.selected_macro_name.get()
        speed = self.speed_input.get()
        try:
            speed = float(speed)
        except ValueError:
            self.logger.error(f"Invalid speed value: {speed}. Using default speed {DEFAULT_SPEED}")
            speed = DEFAULT_SPEED
        self.speed = speed
        if macro_name == NO_MACRO_SELECTED:
            return
        self.hide_window()
        self.play_macro(macro_name)
        self.show_window()

    def play_macro(self, macro_name: str):
        self.logger.debug(f"Playing macro {macro_name}")
        history = self.storage_service.load_history(macro_name=macro_name)
        self.start_exit_key_listener()
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.playback_service.play, args=(history, self.speed, self.stop_event))
        thread.start()
        thread.join()
        self.stop_event = None
        self.stop_exit_key_listener()

    def delete_macro(self):
        macro_name = self.selected_macro_name.get()
        if macro_name == NO_MACRO_SELECTED:
            return
        self.logger.debug(f"Deleting macro {macro_name}")
        self.storage_service.delete_history(macro_name=macro_name)
        self.update_available_macros()
        self.manage_window_popup.destroy()

    def get_available_macros(self) -> List[str]:
        self.logger.debug("Getting available macros")
        macros = self.storage_service.get_available_files()
        self.logger.debug(f"Available macros: {macros}")
        return [NO_MACRO_SELECTED] + macros

    def update_available_macros(self):
        self.selected_macro_name = tk.StringVar()
        self.selected_macro_name.set(NO_MACRO_SELECTED)
        self.available_macro_names = self.get_available_macros()
        self.logger.debug(f"Available macros updated: {self.available_macro_names}")

    def hide_window(self):
        self.logger.debug("Hiding window")
        self.root.withdraw()
        if self.replay_window_popup:
            self.replay_window_popup.withdraw()

    def show_window(self):
        self.root.deiconify()
        if self.replay_window_popup:
            self.replay_window_popup.deiconify()

    def start_listeners(self):
        self.start_exit_key_listener()
        self.listeners_service.start_recording()

    def start_exit_key_listener(self):
        self.exit_key_listener = KeyboardListener(on_press=self.on_press)
        self.exit_key_listener.start()

    def stop_listeners(self):
        self.listeners_service.stop_recording()
        self.stop_exit_key_listener()

    def stop_exit_key_listener(self):
        if self.exit_key_listener:
            self.exit_key_listener.stop()
            self.exit_key_listener = None

    def on_press(self, key):
        if key == self.listeners_service.exit_key:
            self.logger.info("Exiting Copycat")
            if self.stop_event is not None:
                self.logger.debug("Stopping playback")
                self.stop_event.set()
            self.pause()
