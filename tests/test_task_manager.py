import json
import unittest
from datetime import datetime
from unittest.mock import patch

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tasks.task import Task
from tasks.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Sets up test environment by creating a temporary file and a sample of tasks."""
        self.test_file = "test_tasks.json"
        with open(self.test_file, "w") as file:
            json.dump([], file)
        
        self.sample_tasks =[
            Task("Start CS50p", "15/12/2024"),
            Task("Finish all 9 weeks of CS50p", "22/12/2024"),
            Task("Start CS50p final project", "23/12/2024"),
            Task("Finish CS50p final project", "29/12/2024")
        ]
    
    def tearDown(self):
        """Cleans up the test environment by removing the test file if it exists."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_tasks(self):
        """
        Test the functionality of saving tasks to a JSON file.

        This test verifies that:
        1. The task list is correctly converted to a list of dictionaries.
        2. The tasks are correctly saved to the specified JSON file.

        Steps:
        - Call the '_save_tasks' method on the TaskManager with a sample task list.
        - Read the JSON file and compare its content with the expected task list in dictionary format.

        Assertions:
        - The content of the JSON file matches the expected task list.
        """
        # Save tasks to the JSON file
        TaskManager._save_tasks(self.sample_tasks, self.test_file)
        dicts_task_list = [task.to_dict() for task in self.sample_tasks]

        # Read the content of the file and save it in 'data'
        with open(self.test_file, "r") as file:
            data = json.load(file)
        
        # Assert that the tasks saved in the file match the expected task list
        self.assertEqual(data, dicts_task_list, "")
    
    @patch("builtins.print")
    def test_load_file(self, mock_print):
        """
        Test the functionality of loading tasks from a JSON file.

        This test verifies that:
        1. Tasks are correctly loaded from the specified JSON file.
        2. A proper error message is printed if the file does not exist.

        Steps:
        - Call the '_load_file' method on the TaskManager with a valid file.
        - Verify that an empty list is returned when the file is empty.
        - Call the '_load_file' method with a non-existing file and verify the correct error message is printed.

        Assertions:
        - The loaded tasks are an empty list if the file is empty.
        - The correct error message is printed if the file does not exist.
        """
        # Load tasks from the test file and verify the results
        data = TaskManager._load_file(self.test_file)
        self.assertEqual(data, [])
        
        # Try loading a non-existing file and verify the error message
        TaskManager._load_file("non_existing_file.json")
        mock_print.assert_called_with("File to load not found")
    
    def test_init(self):
        """
        Test the initialization of the TaskManager.

        This test verifies that:
        1. The TaskManager instance is correctly initialized with an empty task list if the file is empty or does not exist.

        Steps:
        - Create a TaskManager instance with a test file.
        - Verify that the task list is initialized as empty if the file contains no tasks or doesn't exist.

        Assertions:
        - The TaskManager's task list should be empty upon initialization if no tasks are present in the file.
        """
        # Initialize the TaskManager with the test file
        manager = TaskManager(self.test_file)

        # Assert that the TaskManager's task list is empty if no tasks are loaded
        self.assertEqual(manager.tasks, [], "Tasks have not been initialized")
    
    def test_add_task(self):
        """
        Test the functionality of adding a task to the TaskManager.

        This test verifies that:
        1. A task is successfully added to the TaskManager's internal task list.
        2. The task's data is accurately saved to the JSON file.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add a sample task to the TaskManager.
        - Compare the added task with the expected sample task in the TaskManager's internal state.
        - Read the JSON file to ensure the task was correctly written to the file.

        Assertions:
        - The task in the TaskManager matches the sample task after addition.
        - The task written to the JSON file matches the sample task.
        """
        # Initialize the TaskManager with the test file
        manager = TaskManager(self.test_file)

        # Add a sample task to the manager and save its dictionary representation
        manager.add_task(self.sample_tasks[0])
        manager_task = manager.tasks[0].to_dict()

        # Assert that the task in the TaskManager matches the expected task
        # and ensure it is correctly written to the file
        self.assertEqual(manager_task, self.sample_tasks[0].to_dict(), "The task in the TaskManager does not match the expected task.")
        with open(self.test_file, "r") as file:
            data = json.load(file)

        # Assert that the task written to the JSON file matches the expected task
        self.assertEqual(manager_task, data[0], "The task written to the JSON file does not match the expected task.")
    
    def test_update_task(self):
        """
        Test the functionality of updating a task's completion status.

        This test verifies that:
        1. The task's "completed" status is updated correctly in the TaskManager.
        2. The updated status is saved accurately in the JSON file.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add a sample task to the TaskManager.
        - Update the task's completion status to True.
        - Verify the task's updated status in the TaskManager's internal state.
        - Verify the task's updated status in the JSON file.

        Assertions:
        - The task's "completed" status matches the expected value after updating.
        - The "completed" status in the JSON file matches the expected value.
        """
        # Initialize the TaskManager, add a sample task and get the task id
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[0])
        task_id = manager.tasks[0].id

        # Update the task's status to 'completed' and verify it in the TaskManager
        manager.update_task(task_id, True)
        task_status = manager.tasks[0].completed

        # Assert that the task's status was correctly updated in the TaskManager
        self.assertEqual(task_status, True, "The task's status in the TaskManager is incorrect.")

        # Check that the task's status was correctly written to the JSON file
        with open(self.test_file, "r") as file:
            data = json.load(file)
        self.assertEqual(task_status, data[0]["completed"], "The task's status in the JSON file is incorrect.")
    
    def test_edit_task(self):
        """
        Test the functionality of editing a task's title and deadline.

        This test verifies that:
        1. The task's title and deadline are updated correctly in the TaskManager.
        2. The updated task data is saved accurately in the JSON file.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add a sample task to the TaskManager.
        - Edit the task's title and deadline.
        - Verify the task's updated data in the TaskManager's internal state.
        - Verify the task's updated data in the JSON file.

        Assertions:
        - The task's title and deadline match the expected values after editing.
        - The updated task in the JSON file matches the expected values.
        """
        # Initialize the TaskManager, add a sample task and get the task id
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[0])
        task_id = manager.tasks[0].id
        
        # Define new values for the task title and deadline
        new_title = "Test title edit"
        new_deadline = "25/12/2024"

         # Edit the task and verify that the title and deadline were updated
        manager.edit_task(task_id, new_title, new_deadline)
        task_title = manager.tasks[0].title
        task_deadline = manager.tasks[0].deadline

        # Assert that the task's title and deadline were updated correctly
        self.assertEqual(task_title, new_title, "The task's title is incorrect.")
        self.assertEqual(task_deadline, new_deadline, "The task's deadline is incorrect.")

        # Check that the updated task is correctly written to the JSON file
        with open(self.test_file, "r") as file:
            data = json.load(file)
        self.assertEqual(manager.tasks[0].to_dict(), data[0], "The task data in the JSON file is incorrect.")
    
    def test_remove_task(self):
        """
        Test the functionality of removing a task from the TaskManager.

        This test verifies that:
        1. The specified task is successfully removed from the TaskManager.
        2. The remaining tasks in the TaskManager are updated correctly.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add multiple sample tasks to the TaskManager.
        - Remove the last task.
        - Verify that the removed task is no longer in the TaskManager's internal state.

        Assertions:
        - The new last task in the TaskManager does not match the removed task.
        """
        # Initialize the TaskManager, add two sample tasks and get the last task
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[0])
        manager.add_task(self.sample_tasks[1])
        last_task = manager.tasks[-1]

        # Remove the last task and get the new last task
        manager.remove_task(last_task.id)
        new_last_task = manager.tasks[-1]

        # Assert that the last task was removed correctly
        self.assertNotEqual(new_last_task, last_task, "The task was not removed correctly.")
    
    def test_get_filtered_tasks(self):
        """
        Test the functionality of filtering tasks based on their completion status.

        This test verifies that:
        1. All tasks are returned when filtering with "All".
        2. Only completed tasks are returned when filtering with "Completed".
        3. Only pending tasks are returned when filtering with "Pending".

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add sample tasks to the TaskManager.
        - Modify the completion status of tasks.
        - Retrieve tasks based on different filter criteria and verify the results.

        Assertions:
        - The tasks returned for each filter criteria match the expected results.
        """
        # Initialize the TaskManager and add two sample tasks
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[0])
        manager.add_task(self.sample_tasks[1])

        # Set one task as completed and get the completed task and the not completed task
        manager.tasks[0].completed = True
        task_completed = manager.tasks[0].to_dict()
        task_not_completed = manager.tasks[1].to_dict()

        # Get different filtered task lists: All, Completed, and Pending
        all_tasks = [task.to_dict() for task in manager.get_filtered_tasks("All")]
        completed_tasks = manager.get_filtered_tasks("Completed")
        not_completed_tasks = manager.get_filtered_tasks("Pending")
        
        # Assert that the filtered tasks are correct for each filter type
        self.assertEqual(all_tasks, [task_completed, task_not_completed], "The 'All' filter did not return the correct tasks.")
        self.assertEqual(completed_tasks[0].to_dict(), task_completed, "The 'Completed' filter did not return the correct tasks.")
        self.assertEqual(not_completed_tasks[0].to_dict(), task_not_completed, "The 'Pending' filter did not return the correct tasks.")
    
    def test_search_task(self):
        """
        Test the functionality of searching for tasks based on a query string and filter criteria.

        This test verifies that:
        1. Tasks containing the query string in their title are returned.
        2. Tasks containing the query string and matching the filter criteria are returned.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add sample tasks to the TaskManager.
        - Modify the completion status of tasks.
        - Search tasks using different queries and filter criteria, and verify the results.

        Assertions:
        - The tasks returned for each query and filter combination match the expected results.
        """
        # Initialize the TaskManager and add several sample tasks
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[0])
        manager.add_task(self.sample_tasks[1])
        manager.add_task(self.sample_tasks[2])
        manager.add_task(self.sample_tasks[3])

        # Set the first two tasks as completed
        manager.tasks[0].completed = True
        manager.tasks[1].completed = True

        # Get search queries without filters
        query_1 = [task.to_dict() for task in manager.search_task("st")]
        query_2 = [task.to_dict() for task in manager.search_task("Fin")]
        
        # Get search queries wit filters
        query_3 = [task.to_dict() for task in manager.search_task("st", "Completed")]
        query_4 = [task.to_dict() for task in manager.search_task("Fin", "Pending")]

        dict_tasks = [task.to_dict() for task in manager.tasks]

        # Assert that the search results match the expected tasks
        self.assertEqual(query_1, [dict_tasks[0], dict_tasks[2]], "The search query 'st' did not return the correct tasks.")
        self.assertEqual(query_2, [dict_tasks[1], dict_tasks[3]], "The search query 'Fin' did not return the correct tasks.")
        self.assertEqual(query_3, [dict_tasks[0]], "The filtered search query 'st' with 'Completed' did not return the correct tasks.")
        self.assertEqual(query_4, [dict_tasks[3]], "The filtered search query 'Fin' with 'Pending' did not return the correct tasks.")
    
    def test_sort_tasks_by_date(self):
        """
        Test the functionality of sorting tasks by their deadline.

        This test verifies that:
        1. The tasks are sorted in ascending order of their deadlines.

        Steps:
        - Create a TaskManager instance with a temporary test file.
        - Add sample tasks to the TaskManager in random order of deadlines.
        - Sort the tasks by their deadlines.
        - Verify the sorted order matches the expected order.

        Assertions:
        - The tasks in the TaskManager after sorting match the expected order of deadlines.
        """
        # Initialize the TaskManager and add several sample tasks
        manager = TaskManager(self.test_file)
        manager.add_task(self.sample_tasks[3])
        manager.add_task(self.sample_tasks[1])
        manager.add_task(self.sample_tasks[0])
        manager.add_task(self.sample_tasks[2])

        # Sort tasks by deadline manually
        task_list = manager.tasks
        task_list.sort(key=lambda task: datetime.strptime(task.deadline, "%d/%m/%Y"))
        sorted_tasks = [task.to_dict() for task in task_list]

        # Sort tasks using the method
        manager.sort_tasks_by_date()

        # Assert that the tasks are sorted correctly by deadline
        self.assertEqual([task.to_dict() for task in manager.tasks], sorted_tasks)


if __name__ == "__main__":
    unittest.main()
