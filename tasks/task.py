from __future__ import annotations
from datetime import datetime
import uuid


class Task:
    """
    A class representing a task with attributes like title, deadline, and completion status.
    Each task is assigned a unique identifier (ID) upon creation.

    Attributes:
        id (str): A unique identifier for the task, generated using UUID.
        title (str): The title or name of the task.
        deadline (str): The deadline associated with the task, usually in string format (e.g., "DD-MM-YYYY").
        completed (bool): A flag indicating whether the task has been completed (default is False).

    Methods:
        __str__() -> str:
            Returns a string representation of the task, including the ID, title, and deadline.

        to_dict() -> dict:
            Converts the task object to a dictionary representation, including its ID, title, deadline, and completion status.

        from_dict(data: dict) -> Task:
            Class method to create a Task object from a dictionary.

        _validate_type(value, expected_type, error_message: str) -> None:
            Private Class Method to validate input types

        _validate_date(date: str) -> None:
            Private method to validate dates
    """

    def __init__(self, title: str, deadline: str, completed:bool = False) -> None:
        self._id = str(uuid.uuid4()) # Generates a unique ID
        self.title = title
        self.deadline = deadline
        self.completed = completed

    def __str__(self) -> str:
        return f"Task: {self.title} | {self.deadline} | ID = {self.id}"

    def to_dict(self) -> dict:
        """
        Converts the task object to a dictionary.

        Returns:
            dict: A dictionary containing the task's ID, title, deadline and completion status.
        """
        return {
            "id": self.id,
            "title": self.title,
            "deadline": self.deadline,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict[Task]) -> Task:
        """
        Creates a Task object from a dictionary.

        Args:
            data (dict): A dictionary containing the task's attributes (id, title, deadline, and completed).

        Raises:
            TypeError: If the value is not an instance of the expected type
            ValueError: If the data keys is invalid.

        Returns:
            Task: A new Task instance created from the dictionary data.

        """
        cls._validate_type(data, dict, f"Invalid JSON structure: Expected a Dict, not a {type(data).__name__}")
        required_keys = ['id', 'title', 'deadline', 'completed']
        if not (set(data.keys()) == set(required_keys)):
            raise ValueError(f"Invalid data keys: Expected {required_keys}, but found {list(data.keys())}")
        task = cls(data["title"], data["deadline"], data["completed"])
        task._id = data["id"]
        return task

    # Getters and Setters for each property
    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        Task._validate_type(title, str, "Invalid value for 'title': Expected a str, not a ")
        self._title = title

    @property
    def deadline(self) -> str:
        return self._deadline

    @deadline.setter
    def deadline(self, deadline: str) -> None:
        Task._validate_type(deadline, str, f"Invalid value for 'title': Expected a str, not a {type(deadline).__name__}")
        self._validate_date(deadline)
        self._deadline = deadline

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, completed: bool) -> None:
        Task._validate_type(completed, bool, f"Invalid value for 'completed': Expected a boolean, not a {type(completed).__name__}.")
        self._completed = completed

    # PRIVATE METHODS
    @classmethod
    def _validate_type(cls, value, expected_type, error_message: str) -> None:
        """
        Private class method to validate the type of an input value.

        This method checks if the provided value is an instance of the expected type.
        If the value is not of the expected type, a TypeError is raised with a custom error message.

        Args:
            value: The value to be checked. Can be of any type.
            expected_type: The type that the value is expected to be. Typically, this will be a Python type like str, int, etc.
            error_message: A string message that will be included in the TypeError if the validation fails.

        Raises:
            TypeError: If the value is not an instance of the expected type.
        """
        if not isinstance(value, expected_type):
            raise TypeError(error_message)

    def _validate_date(self, date: str) -> None:
        """
        Private method to validate the date format "dd/mm/YYYY".

        Args:
            date_str (str): The date string to validate.

        Raises:
            ValueError: If the date string does not match the expected format or is invalid.
        """
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Invalid value for 'deadline': Expected a valid date in the pattern 'dd/mm/YYYY', but got '{date}'.")
