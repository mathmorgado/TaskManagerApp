import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tasks.task_manager import TaskManager
from tasks.task import Task


class TodoApp:
    """
    A GUI application for managing tasks using CustomTkinter.

    Attributes:
        task_manager (TaskManager): Manages tasks' data and operations.
        root (CTk): The root window for the application.
        selected_task (str): The title of the currently selected task.
        filtred_type (str): The current filter type for displaying tasks.

    Methods:
        __init__(root, storage_path) -> None:
            Initializes the application.

        load_tasks(filter_type="All", query=None) -> None:
            Loads and displays tasks based on filters or search queries.

        add_task_to_ui(task, filter_type) -> None:
            Adds a task to the UI, considering the filter type.

        delete_task() -> None:
            Deletes the selected task from the UI.

        open_add_task_window() -> None:
            Opens a window to add a new task.

        open_edit_task_window() -> None:
            Opens a window to edit the selected task.

        open_entry_windows(title, edit=False, task_to_edit=None) -> None:
            Opens a window for adding or editing tasks based on the provided parameters.

        filter_tasks(filter_type) -> None:
            Applies a filter to the displayed tasks based on their completion status.

        search_task(event) -> None:
            Searches for tasks based on a query entered in the search bar.
    """

    def __init__(self, root, storage_path) -> None:
        # Task Manager initialization
        self.task_manager = TaskManager(storage_path)

        # Root window configuration
        self.root = root
        self.root.title("TODO LIST")
        self.root.geometry("460x600")
        self.root.resizable(False, False)

        # Configure appearance settings
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

         # Holds the currently selected task
        self.selected_task = None

        # Holds the currently selected frame task
        self.selected_task_frame = None

        # Title section at the top of the window
        self.title_frame = ctk.CTkFrame(root, fg_color="#576cd6", height=70)
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Title label
        self.title_label = ctk.CTkLabel(
            self.title_frame, text="TODO LIST", font=("Arial", 20, "bold"), text_color="#ffffff"
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Search bar to filter tasks dynamically
        self.search_entry = ctk.CTkEntry(root, placeholder_text="Search Task", width=250)
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_task)

        # ADD button which triggers the 'open_add_task_window' function when clicked
        self.add_button = ctk.CTkButton(root, text="ADD", width=80, command=self.open_add_task_window)
        self.add_button.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Create a filter menu with options to filter tasks
        self.filter_menu = ctk.CTkOptionMenu(
            root, values=["All", "Completed", "Pending"], width=80, command=self.filter_tasks
        )
        self.filter_menu.grid(row=1, column=2, padx=5, pady=10, sticky="w")

        # Initialize the default filter to "All"
        self.filtred_type = "All"

        # Label to display "Tasks" with a bold font
        self.tasks_label = ctk.CTkLabel(root, text="Tasks", font=("Arial", 16, "bold"), text_color="#333333")
        self.tasks_label.grid(row=2, column=0, columnspan=3, pady=10, sticky="w", padx=10)

        # Frame to hold the task elements (e.g., task list), with a transparent background
        self.tasks_frame = ctk.CTkFrame(root, fg_color="transparent", width=620, height=400)
        self.tasks_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # DELETE button which triggers the 'delete_task' function when clicked
        self.delete_button = ctk.CTkButton(root, text="DELETE", fg_color="#ff4d4d", width=90, command=self.delete_task)
        self.delete_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # EDIT button which triggers the 'open_edit_task_window' function when clicked
        self.edit_button = ctk.CTkButton(root, text="EDIT", fg_color="#ff4d4d", width=90, command=self.open_edit_task_window)
        self.edit_button.grid(row=4, column=0, padx=(110, 0), pady=10, sticky="w")

        self.load_tasks()

    def load_tasks(self, filter_type="All", query=None) -> None:
        """
        Loads and displays tasks in the UI based on the given filter and search query.

        Args:
            filter_type (str): The type of tasks to filter. Options include "All", "Completed", and "Pending".
            query (str): A search query to filter tasks by title.

        Behavior:
            - Clears all current task widgets from the UI.
            - Sorts tasks by date before displaying.
            - Filters tasks based on `filter_type` or `query`.
            - Calls `add_task_to_ui` to render each task on the screen.
        """
        # Clear existing widgets in the tasks frame
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Sort tasks by date
        self.task_manager.sort_tasks_by_date()

         # Load tasks based on filters or query
        if not query:
            tasks = self.task_manager.get_filtered_tasks(filter_type)
            for task in tasks:
                self.add_task_to_ui(task, filter_type)
        else:
            tasks = self.task_manager.search_task(query, filter_type)
            for task in tasks:
                self.add_task_to_ui(task, filter_type)


    def add_task_to_ui(self, task, filter_type) -> None:
        """
        Adds a single task to the UI as a frame with interactive elements.

        Args:
            task (Task): The task object to display.
            filter_type (str): The current filter type applied to the task list.

        Behavior:
            - Creates a frame for the task with a checkbox, title, and deadline.
            - Handles task selection when clicked.
            - Toggles the completion state of the task using a checkbox.
        """
        # Create a frame for the task
        task_frame = ctk.CTkFrame(self.tasks_frame, fg_color="white", corner_radius=0, height=50)
        task_frame.pack(fill="x", pady=1)

        # Handle task selection on click
        def select_task(event) -> None:
            # If a task was previously selected, reset its color to "white"
            if self.selected_task_frame:
                self.selected_task_frame.configure(fg_color="white")

            # Select the new task and change its color to "lightblue"
            task_frame.configure(fg_color="lightblue")

            # Update the selected task's ID
            self.selected_task = task.id

            # Store the reference of the currently selected task frame
            self.selected_task_frame = task_frame
        
        def on_enter(event, widget):
            # If the task is not selected, change its color to "lightblue" on mouse hover
            if widget != task_frame or self.selected_task != task.id:
                widget.configure(fg_color="lightblue")

        def on_leave(event, widget):
            # If the task is not selected, change its color back to "white" when the mouse leaves
            if widget != task_frame or self.selected_task != task.id:
                widget.configure(fg_color="white")

        # Binding click event to select the task
        task_frame.bind("<Button-1>", select_task)

        # Binding mouse enter and leave events to change color
        task_frame.bind("<Enter>", lambda event, widget=task_frame: on_enter(event, widget))
        task_frame.bind("<Leave>", lambda event, widget=task_frame: on_leave(event, widget))

        # Create a checkbox to toggle task completion
        checkbox_var = ctk.BooleanVar(value=task.completed)

        def toggle_completion() -> None:
            """
            Toggles the task's completion status and updates the UI and task data.
            """
            task.completed = checkbox_var.get()
            self.task_manager.update_task(task.title, completed=task.completed)
            self.load_tasks(filter_type)

        checkbox = ctk.CTkCheckBox(
            task_frame,
            text=task.title,
            variable=checkbox_var,
            font=("Arial", 14, "bold"),
            text_color="black" if not task.completed else "#777777",
            width=10,
            command=toggle_completion
        )
        checkbox.pack(side="left", padx=5)

        # Display the task's deadline
        task_date_label = ctk.CTkLabel(
            task_frame, text=task.deadline, font=("Arial", 12), text_color="#888888"
        )
        task_date_label.pack(side="right", padx=10)

        # Add an underline to visually separate tasks
        underline = ctk.CTkFrame(task_frame, fg_color="#cccccc", height=1)
        underline.pack(fill="x", side="bottom")

    def delete_task(self) -> None:
        """
        Deletes the currently selected task.

        Behavior:
            - Shows a warning if no task is selected.
            - Removes the selected task from the task manager.
            - Refreshes the task list in the UI.
        """
        # Check if a task is selected
        if not self.selected_task:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return

        # Remove the selected task and reset the selection
        self.task_manager.remove_task(self.selected_task)
        self.selected_task = None

        # Reload tasks with the current filter applied
        self.load_tasks(self.filtred_type)

    def open_add_task_window(self) -> None:
        """
        Opens a new window for adding a task.
        """
        self.open_entry_windows("Add task")

    def open_edit_task_window(self) -> None:
        """
        Opens a window to edit the selected task.

        Behavior:
            - Validates that a task is selected.
            - Finds the corresponding task object in the task manager.
            - Calls `open_entry_windows` with the appropriate title and edit mode.
        """
        # Validate task selection
        if not self.selected_task:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return

        # Find the task to edit
        task_to_edit = None
        for task in self.task_manager.tasks:
            if task.id == self.selected_task:
                task_to_edit = task
                break

        # Handle missing task case
        if not task_to_edit:
            messagebox.showerror("Error", "Selected task not found.")
            return

        # Open the entry window in edit mode
        self.open_entry_windows("Edit task", edit=True, task_to_edit=task_to_edit)

    def open_entry_windows(self, title, edit=False, task_to_edit=None) -> None:
        """
        Opens a window for adding or editing a task.

        Args:
            title (str): The title of the window ("Add Task" or "Edit Task").
            edit (bool): If True, opens the window in edit mode with pre-filled fields.
            task_to_edit (Task): The task object to edit. Only used if `edit` is True.

        Behavior:
            - Ensures that only one task entry window can be open at a time.
            - Provides input fields for task title and deadline.
            - Includes a calendar widget for selecting a date.
            - Saves the new or edited task after validation.
        """

        # Ensures only one window is open at a time.
        if hasattr(self, "add_window") and self.add_window.winfo_exists():
            messagebox.showwarning("Warning", "Close the current window before opening a new one.")
            return

        # Create the new window
        add_window = ctk.CTkToplevel(self.root)
        add_window.title(title)
        add_window.geometry("400x400")

        # Input field for task title
        title_label = ctk.CTkLabel(add_window, text="Title:")
        title_label.pack(pady=1)
        title_entry = ctk.CTkEntry(add_window, width=250)
        title_entry.pack(pady=10)

        # Input field for task deadline
        deadline_label = ctk.CTkLabel(add_window, text="Deadline:")
        deadline_label.pack(pady=1)

        # Calendar widget for date selection
        self.calendar = Calendar(add_window, date_pattern="dd/mm/yyyy", height=300, width=300)
        self.calendar.pack(pady=5)

        # Read-only entry to display the selected date
        deadline_entry = ctk.CTkEntry(add_window, width=250, state="readonly")
        deadline_entry.pack(pady=5)

        # If editing, pre-fill the fields with existing task data
        if edit:
            title_entry.insert(0, task_to_edit.title)
            deadline_entry.configure(state="normal")
            deadline_entry.insert(0, task_to_edit.deadline)
            deadline_entry.configure(state="readonly")

        def on_date_select(event) -> None:
            """
            Updates the deadline field when a date is selected in the calendar.
            """
            self.selected_date = self.calendar.get_date()
            deadline_entry.configure(state="normal")
            deadline_entry.delete(0, ctk.END)
            deadline_entry.insert(0, self.selected_date)
            deadline_entry.configure(state="readonly")

        # Bind the date selection event to update the deadline field
        self.calendar.bind("<<CalendarSelected>>", on_date_select)

        def save_task() -> None:
            """
            Saves the new or edited task after validation.
            """
            title = title_entry.get()
            deadline = deadline_entry.get()

            if not title or not deadline:
                messagebox.showwarning("Warning", "All fields are required.")
                return

            if edit:
                self.task_manager.edit_task(self.selected_task, title, deadline)
            else:
                new_task = Task(title, deadline)
                self.task_manager.add_task(new_task)
            self.load_tasks(self.filtred_type)
            add_window.destroy()

        # Button to save the task
        add_button = ctk.CTkButton(add_window, text=title, command=save_task)
        add_button.pack(pady=10)

    def filter_tasks(self, filter_type) -> None:
        """
        Applies a filter to the displayed tasks.

        Args:
            filter_type (str): The type of tasks to filter. Options include "All", "Completed", and "Pending".

        Behavior:
            - Updates the `filtred_type` attribute with the selected filter type.
            - Reloads the tasks based on the selected filter.
        """
        self.filtred_type = filter_type
        self.load_tasks(filter_type, query=self.search_entry.get())

    def search_task(self, event) -> None:
        """
        Searches for tasks based on the query entered in the search bar.

        Args:
            event: The key release event triggered when the user types in the search bar.

        Behavior:
            - Retrieves the search query from the search bar.
            - Calls `load_tasks` to update the displayed tasks based on the query and current filter.
        """
        query = self.search_entry.get()
        self.load_tasks(filter_type=self.filtred_type, query=query)
