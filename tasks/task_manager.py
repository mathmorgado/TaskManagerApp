from __future__ import annotations
from datetime import datetime
from typing import List
import re

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tasks.task import Task
from storage.file_manager import FileManager


class TaskManager:
    """
    Manages a collection of tasks, providing functionalities to add, edit, remove,
    filter, search, and sort tasks. The tasks are stored in a file specified by the
    'file_name' parameter.

    Attributes:
    - file_name (str): The name of the file where tasks are stored.
    - tasks (List[Task]): A list of Task objects managed by the TaskManager.

    Methods:
        __init__(file_name: str) -> None:
            Initializes the TaskManager with the specified file and loads any existing tasks.

        add_task(task: Task) -> None:
            Adds a new task to the manager and saves the updated task list to the file.

        update_task(task_id: str, completed: bool = False) -> None:
            Updates the completion status of a task identified by its ID.

        edit_task(task_id: str, new_title: str, new_deadline: str) -> None:
            Edits the title and deadline of a task identified by its ID.

        remove_task(task_id: str) -> None:
            Removes a task identified by its ID from the manager and updates the file.

        get_filtered_tasks(filter_type: str = "All") -> List[Task]:
            Returns a list of tasks filtered by their completion status.

        search_task(query: str, filter_type: str = "All") -> List[Task]:
            Searches for tasks based on a query string and an optional filter.

        sort_tasks_by_date() -> None:
            Sorts the tasks by their deadline in ascending order and updates the file.

        _load_file(file: str) -> List[Task]:
            Loads tasks from the specified file and converts them into Task objects.

        _save_tasks(tasks_list: List[Task], file: str, ) -> None:
            Saves the current list of tasks to the file in a dictionary format.
    """

    def __init__(self, file_name: str) -> None:
        """
        Initializes the TaskManager by loading tasks from the specified file.

        Args:
            file_name (str): The name of the file to load tasks from and save to.
        """
        self.file_name = file_name
        self.tasks: List[Task] = self._load_file(self.file_name)

    def add_task(self, task: Task) -> None:
        """
        Adds a new task to the list of tasks and saves the updated list to the file.

        Args:
        - task (Task): The Task object to be added.
        """
        self.tasks.append(task)
        self._save_tasks(self.tasks, self.file_name)

    def update_task(self, task_id: str, completed:bool = False) -> None:
        """
        Updates the completion status of a task based on its ID.

        Args:
        - task_id (str): The ID of the task to be updated.
        - completed (bool, optional): The new completion status of the task. Default is False.
        """
        for task in self.tasks:
            if task.id == task_id:
                if completed:
                    task.completed = completed
                self._save_tasks(self.tasks, self.file_name)
                return

    def edit_task(self, task_id: str, new_title: str, new_deadline: str) -> None:
        """
        Edits the title and deadline of a task based on its ID.

        Args:
        - task_id (str): The ID of the task to be edited.
        - new_title (str): The new title for the task.
        - new_deadline (str): The new deadline for the task in the format "%d/%m/%Y".
        """
        for task in self.tasks:
            if task.id == task_id:
                task.title = new_title
                task.deadline = new_deadline
                self._save_tasks(self.tasks, self.file_name)
                return

    def remove_task(self, task_id: int) -> None:
        """
        Removes a task from the task list based on its ID and saves the updated list.

        Args:
        - task_id (int): The ID of the task to be removed.
        """
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks(self.tasks, self.file_name)

    def get_filtered_tasks(self, filter_type:str = "All") -> List[Task]:
        """
        Returns a list of tasks filtered by the specified status: "All", "Completed",
        or "Pending".

        Args:
        - filter_type (str, optional): The filter criteria. Default is "All".

        Returns:
        - List[Task]: A list of tasks that match the filter criteria.
        """
        if filter_type == "Completed":
            return [task for task in self.tasks if task.completed]
        elif filter_type == "Pending":
            return [task for task in self.tasks if not task.completed]
        return self.tasks

    def search_task(self, query: str, filter_type:str = "All") -> List[Task]:
        """
        Searches for tasks whose title starts with the given query string, optionally
        filtered by task status.

        Args:
        - query (str): The query string to search for in task titles.
        - filter_type (str, optional): The filter criteria for the tasks. Default is "All".

        Returns:
        - List[Task]: A list of tasks matching the search query.
        """
        tasks = self.get_filtered_tasks(filter_type)
        return[task for task in tasks if task.title.lower().startswith(query.lower())]

    def sort_tasks_by_date(self) -> None:
        """
        Sorts the tasks by their deadline in ascending order and saves the updated list.
        """
        self.tasks.sort(key=lambda task: datetime.strptime(task.deadline, "%d/%m/%Y"))
        self._save_tasks(self.tasks, self.file_name)

    # PRIVATE METHODS
    @staticmethod
    def _load_file(file: str) -> List[Task]:
        """
        Loads the tasks from the specified file and returns them as a list of Task objects.

        Returns:
        - List[Task]: A list of Task objects loaded from the file.
        """
        tasks_dicts = FileManager.load_from_file(file)
        return [Task.from_dict(task_dict) for task_dict in tasks_dicts]

    @staticmethod
    def _save_tasks(tasks_list: List[Task], file: str) -> None:
        """
        Saves the current list of tasks to the file in dictionary format.
        """
        tasks_dicts = [task.to_dict() for task in tasks_list]
        FileManager.save_to_file(tasks_dicts, file)

    # Getter and Setter
    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name) -> None:
        if not (matche := re.search(r"^[a-zA-Z0-9_\-/]+\.json$", file_name)):
            raise ValueError(f"Invalid value for 'file_name': Expected a string ending with '.json', but got '{file_name}'.")

        self._file_name = file_name
