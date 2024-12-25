import unittest
import json
import os

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from storage.file_manager import FileManager


class TestFileManager(unittest.TestCase):

    def setUp(self):
        """Sets up test environment by creating a temporary file path."""
        self.test_file = "test_tasks.json"
        self.sample_tasks = [
            {"title": "Task 1", "deadline": "2024-12-24"},
            {"title": "Task 2", "deadline": "2024-12-25"}
        ]

    def tearDown(self):
        """Cleans up the test environment by removing the test file if it exists."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_to_file(self):
        """
        Test the functionality of saving tasks to a file.

        This test verifies that:
        1. The tasks are correctly saved to a file.
        2. The file is created and contains the correct task data.

        Steps:
        - Save the sample tasks to a file using the 'save_to_file' method.
        - Check that the file is created.
        - Read the file content and ensure it matches the expected task data.

        Assertions:
        - The file should be created.
        - The content of the file should match the sample tasks.
        """
        # Save the sample tasks to a file using the 'save_to_file' method and check if the file was created
        FileManager.save_to_file(self.sample_tasks, self.test_file)
        self.assertTrue(os.path.exists(self.test_file), "The file was not created.")

        # Read the content of the file and verify if it matches the expected task data
        with open(self.test_file, "r") as file:
            data = json.load(file)
        self.assertEqual(data, self.sample_tasks, "The tasks were not correctly saved to the file.")

    def test_load_from_file(self):
        """
        Test the functionality of loading tasks from a file.

        This test verifies that:
        1. The tasks are correctly loaded from a file.
        2. The loaded tasks match the expected task data.

        Steps:
        - Write the sample tasks to a file.
        - Load the tasks from the file using the 'load_from_file' method.
        - Compare the loaded tasks with the expected sample tasks.

        Assertions:
        - The tasks loaded from the file should match the expected tasks.
        """
        with open(self.test_file, "w") as file:
            json.dump(self.sample_tasks, file)

        # Load the tasks from the file and verify that they match the expected tasks
        loaded_tasks = FileManager.load_from_file(self.test_file)
        self.assertEqual(loaded_tasks, self.sample_tasks, "The tasks were not correctly loaded from the file.")

    def test_load_from_nonexistent_file(self):
        """
        Test the behavior when attempting to load tasks from a nonexistent file.

        This test verifies that:
        1. The method correctly handles the case when the file does not exist.
        2. An empty list is returned when the file is nonexistent.

        Steps:
        - Attempt to load tasks from a nonexistent file.
        - Verify that an empty list is returned.

        Assertions:
        - The method should return an empty list when the file does not exist.
        """
        loaded_tasks = FileManager.load_from_file("nonexistent_file.json")
        self.assertEqual(loaded_tasks, [], "The method did not return an empty list for a nonexistent file")

    def test_load_from_invalid_json(self):
        """
        Test the behavior when the file contains invalid JSON.

        This test verifies that:
        1. The method handles invalid JSON files gracefully.
        2. An empty list is returned when the file contains invalid JSON.

        Steps:
        - Write invalid JSON content to the file.
        - Attempt to load the tasks from the file.
        - Verify that an empty list is returned.

        Assertions:
        - The method should return an empty list when the file contains invalid JSON.
        """
        # Write invalid JSON content to the file
        with open(self.test_file, "w") as file:
            file.write("Invalid JSON content")

        # Attempt to load tasks from the invalid JSON file and verify that an empty list is returned
        loaded_tasks = FileManager.load_from_file(self.test_file)
        self.assertEqual(loaded_tasks, [], "The method did not return an empty list for a file with invalid JSON.")


if __name__ == "__main__":
    unittest.main()
