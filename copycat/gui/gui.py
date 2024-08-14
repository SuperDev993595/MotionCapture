import tkinter as tk
from textwrap import dedent
from tkinter import ttk
from typing import Callable

from ttkthemes.themed_tk import ThemedTk

from copycat.shared.utils.logger import Logger
from services.listeners_service import ListenersService

description = dedent("""
Copycat is a simple macro recorder and player tool.
It allows you to record your keyboard and mouse inputs and play them back.
No tutorial needed, just start recording and play it back.

More information can be found at https://github.com/ZappaBoy/copycat
Feel free to contribute to the project, open an issue or simply buy me a coffee.

Copycat was created by ZappaBoy. 
""")


class Gui:
    def __init__(self):
        self.logger = Logger()
        self.width = 700
        self.height = 40
        self.geometry = f"{self.width}x{self.height}"
        self.window_title = "Copycat"
        self.theme = "equilux"
        self.root: tk.Tk | None = None
        self.logger.info("GUI initialized")
        self.listeners_service = ListenersService()

    def record(self):
        self.logger.info("Recording new macro")
        self.listeners_service.start_listeners()

    def pause(self):
        self.logger.info("Pausing macro")
        self.listeners_service.stop_listener()

    def save(self):
        self.logger.info("Saving macro")
        history = self.listeners_service.get_history()
        self.logger.debug(f"History: {history}")
        self.listeners_service.clean_history()
        self.listeners_service.stop_listener()

    def discard(self):
        self.logger.info("Discarding macro")
        self.listeners_service.clean_history()
        self.listeners_service.stop_listener()

    def replay(self):
        self.logger.info("Replaying macro")

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
        self.build_command_button(self.show_info, text="Info")
        self.build_command_button(self.close_window, text="Close")
        return toolbar

    @staticmethod
    def build_command_button(command: Callable, text: str = None) -> tk.Button:
        button = ttk.Button(text=text, command=command, width=10, padding=5)
        button.pack(side=tk.LEFT, expand=True)
        return button

    def show_info_popup(self):
        window = tk.Toplevel(self.root)
        window.title("Info")
        window.geometry("600x260")
        window.resizable(False, False)
        label = tk.Label(window, text=description)
        label.pack()
        button = ttk.Button(window, text="Close", command=window.destroy)
        button.pack()
        window.mainloop()
