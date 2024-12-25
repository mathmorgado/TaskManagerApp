import sys
from pathlib import Path

# Adiciona o diretório raiz ao sys.path (CS50p2024/project/)
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from typing import List, Dict
from tasks.task import Task

class FileManager:
    """
    A utility class for managing file operations, including saving and loading task data to and from files.
    The class supports operations for writing tasks to a file and reading tasks from a file in JSON format.

    Methods:
        save_to_file(tasks: List[Dict], file_name: str) -> None:
            Saves a list of tasks (in dictionary format) to a specified file.

        load_from_file(file_name: str) -> List:
            Loads and returns a list of tasks from the specified file. If the file is not found, returns an empty list.
    """

    @staticmethod
    def save_to_file(tasks: List[Dict], file_name: str) -> None:
        """
        Saves the provided list of tasks (in dictionary format) to the specified file.

        Args:
            tasks (List[Dict]): A list of task dictionaries to be saved.
            file_name (str): The name of the file where the tasks should be saved.
        """
        with open(file_name, "w") as file:
            json.dump(tasks, file, indent=4)

    @staticmethod
    def load_from_file(file_name: str) -> List[Dict]:
        """
        Loads a list of tasks from the specified file. If the file is not found, an empty list is returned.

        Args:
            file_name (str): The name of the file from which to load the tasks.

        Returns:
            List: A list of task dictionaries loaded from the file, or an empty list if the file is not found.
        """
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File to load not found")
            return []
        except json.JSONDecodeError:
            print("File contains invalid JSON")
            return []
            