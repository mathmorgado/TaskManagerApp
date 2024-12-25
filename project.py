from interface.todo_app import TodoApp
import customtkinter as ctk
from pathlib import Path


def main():
    root = ctk.CTk()
    app = TodoApp(root, "storage/task_list.json")
    root.mainloop()


if __name__ == "__main__":
    main()
