# To-Do List with Graphical Interface

This is the final project for the CS50p course, where I created a To-Do list application with a graphical interface. The app follows a CRUD (Create, Read, Update, Delete) model and includes a task management system with search functionality, filters for completed, uncompleted, and all tasks, and ordering by deadline.

## ⚙️ Features

- **CRUD Operations**: Create, Read, Update, and Delete tasks.
- **Search Functionality**: Search for tasks by title.
- **Filters**: View tasks by status — completed, uncompleted, or all tasks.
- **Sorting**: Tasks are ordered by their deadline.
- **Graphical Interface**: The app uses the CustomTKinter library to create an intuitive and interactive user interface.

## 🛠️ Technologies Used

- **Python 3.13.0**
- **CustomTKinter**: For building the graphical interface.
- **TKCalendar**: For building the graphical calendar.
- **JSON**: For saving and loading task data.
- **unittest**: For testing the code.

## 📝 Project Structure

The project is organized into four main directories:

### 1. **Task Directory**
   - **task.py**: Contains the `Task` class, responsible for managing individual tasks (title, deadline, completion status).
   - **task_manager.py**: Contains the `TaskManager` class, which handles the overall task management (filters, search, ordering, CRUD operations).

### 2. **Storage Directory**
   - **tasks.json**: A JSON file used for saving and loading the list of tasks.
   - **file_manager.py**: Contains the `FileManager` class, responsible for loading and saving the tasks to the `tasks.json` file.

### 3. **Interface Directory**
   - **todo_app.py**: Contains the `TodoApp` class, where all the logic of the graphical interface is implemented.

### 4. **Tests Directory**
   - **test_task.py**: Contains unit tests for the Task class, including tests for initialization, methods like to_dict, from_dict, and property validations
   - **test_task_manager.py**: Contains unit tests for the TaskManager class. Tests CRUD operations (Create, Read, Update, Delete) for managing tasks, as well as additional functionalities like filtering, searching, and sorting tasks. It also covers file operations for saving and loading tasks.
   - **test_file_manager.py**: Contains unit tests for the FileManager class, which manages saving and loading tasks from files.

## 📑 Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/todo-list.git
    cd todo-list
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python project.py
    ```
# To-Do List with Graphical Interface

This is the final project for the CS50p course, where I created a To-Do list application with a graphical interface. The app follows a CRUD (Create, Read, Update, Delete) model and includes a task management system with search functionality, filters for completed, uncompleted, and all tasks, and ordering by deadline.

## ⚙️ Features

- **CRUD Operations**: Create, Read, Update, and Delete tasks.
- **Search Functionality**: Search for tasks by title.
- **Filters**: View tasks by status — completed, uncompleted, or all tasks.
- **Sorting**: Tasks are ordered by their deadline.
- **Graphical Interface**: The app uses the CustomTKinter library to create an intuitive and interactive user interface.

## 🛠️ Technologies Used

- **Python 3.13.0**
- **CustomTKinter**: For building the graphical interface.
- **TKCalendar**: For building the graphical calendar.
- **JSON**: For saving and loading task data.
- **unittest**: For testing the code.

## 📝 Project Structure

The project is organized into four main directories:

### 1. **Task Directory**
   - **task.py**: Contains the `Task` class, responsible for managing individual tasks (title, deadline, completion status).
   - **task_manager.py**: Contains the `TaskManager` class, which handles the overall task management (filters, search, ordering, CRUD operations).

### 2. **Storage Directory**
   - **tasks.json**: A JSON file used for saving and loading the list of tasks.
   - **file_manager.py**: Contains the `FileManager` class, responsible for loading and saving the tasks to the `tasks.json` file.

### 3. **Interface Directory**
   - **todo_app.py**: Contains the `TodoApp` class, where all the logic of the graphical interface is implemented.

### 4. **Tests Directory**
   - **test_task.py**: Contains unit tests for the Task class, including tests for initialization, methods like to_dict, from_dict, and property validations
   - **test_task_manager.py**: Contains unit tests for the TaskManager class. Tests CRUD operations (Create, Read, Update, Delete) for managing tasks, as well as additional functionalities like filtering, searching, and sorting tasks. It also covers file operations for saving and loading tasks.
   - **test_file_manager.py**: Contains unit tests for the FileManager class, which manages saving and loading tasks from files.

## 📑 Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/todo-list.git
    cd todo-list
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python project.py
    ```
