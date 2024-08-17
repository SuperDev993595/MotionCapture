import os.path
from typing import List

import joblib

from copycat.models.history.history import History
from copycat.shared.utils.logger import Logger

EXTENSION = "joblib"

class StorageService:

    def __init__(self):
        self.logger = Logger()
        self.config_dir = os.path.join(os.path.expanduser("~"), ".config", "copycat")
        os.makedirs(self.config_dir, exist_ok=True)

    def get_filename(self, name: str) -> str:
        return os.path.join(self.config_dir, f"{name}.{EXTENSION}")

    def save_history(self, macro_name: str, data: History) -> None:
        filename = self.get_filename(macro_name)
        self.logger.info(f"Saving file {filename}")
        with open(filename, "wb") as file:
            joblib.dump(data, file)
            self.logger.info(f"File {filename} saved")

    def delete_history(self, macro_name: str) -> None:
        filename = self.get_filename(macro_name)
        self.logger.info(f"Deleting file {filename}")
        os.remove(filename)

    def load_history(self, macro_name: str) -> History:
        filename = self.get_filename(macro_name)
        self.logger.info(f"Loading file {filename}")
        with open(filename, "rb") as file:
            return joblib.load(file)

    def get_available_files(self) -> List[str]:
        file_list = os.listdir(self.config_dir)
        return [name.replace(f".{EXTENSION}", "") for name in file_list]
