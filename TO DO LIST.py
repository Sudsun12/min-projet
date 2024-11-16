import json
import os
from datetime import datetime

# Simple To-Do List Application in Python

# A dictionary to store tasks with unique IDs
tasks = {}

# File path for saving tasks
file_path = "tasks.json"

def load_tasks():
    """Load tasks from a JSON file."""
    global tasks
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            tasks = json.load(file)
    else:
        tasks = {}

def save_tasks():
    """Save tasks to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

def display_menu():
    print("\nTo-Do List Application")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Complete Task")
    print("6. Exit")

def add_task():
    task_id = len(tasks) + 1
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    
    # Validation de la priorité
    priority_options = {"1": "one", "2": "two", "3": "three"}
    priority = ""
    while priority not in priority_options.values():
        print("Choose priority: 1. One  2. Two  3. Three")
        priority_input = input("Enter priority (1/2/3): ")
        if priority_input in priority_options:
            priority = priority_options[priority_input]
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    due_date = input("Enter due date (YYYY-MM-DD): ")
    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    save_tasks()
    print(f"Task '{title}' added successfully.")

def view_tasks():
    if not tasks:
        print("No tasks found.")
    else:
        for task_id, task_info in tasks.items():
            due_date = datetime.strptime(task_info['due_date'], "%Y-%m-%d")
            days_remaining = (due_date - datetime.now()).days
            print(f"\nTask ID: {task_id}")
            print(f"Title: {task_info['title']}")
            print(f"Description: {task_info['description']}")
            print(f"Priority: {task_info['priority']}")
            print(f"Due Date: {task_info['due_date']}")
            print(f"Days Remaining: {days_remaining} days")
            print(f"Completed: {'Yes' if task_info['completed'] else 'No'}")

def update_task():
    task_id = int(input("Enter the task ID to update: "))
    if task_id in tasks:
        title = input("Enter new title (or press Enter to skip): ")
        description = input("Enter new description (or press Enter to skip): ")
        priority = input("Enter new priority (High/Medium/Low) (or press Enter to skip): ")
        completed = input("Is the task completed? (yes/no): ").lower() == 'yes'

        # Update fields if they were changed
        if title:
            tasks[task_id]["title"] = title
        if description:
            tasks[task_id]["description"] = description
        if priority:
            tasks[task_id]["priority"] = priority
        tasks[task_id]["completed"] = completed

        save_tasks()
        print("Task updated successfully.")
    else:
        print("Task not found.")

def delete_task():
    task_id = int(input("Enter the task ID to delete: "))
    if task_id in tasks:
        del tasks[task_id]
        save_tasks()
        print("Task deleted successfully.")
    else:
        print("Task not found.")

def complete_task():
    task_id = int(input("Enter the task ID to complete: "))
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        save_tasks()
        print("Task marked as completed.")
    else:
        print("Task not found.")

def main():
    load_tasks()
    while True:
        display_menu()
        choice = input("Choose an option (1-6): ")
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            update_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            complete_task()
        elif choice == '6':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the To-Do List application
main()