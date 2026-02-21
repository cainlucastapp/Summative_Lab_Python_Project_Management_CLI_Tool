# lib/controllers/tasks_controller.py

# Requires
from lib.models.task import Task
from lib.utils import storage


class TasksController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []


    # Load data
    def __enter__(self):
        self.data = [Task.from_dict(task) for task in storage.load_data(self.file_path)]
        return self
 

    # Save data
    def __exit__(self, exc_type, exc_value, ex_tb):
        storage.save_data(self.file_path, [task.to_dict() for task in self.data])
    

    # Add task
    def add_task(self, args, users_controller, projects_controller):
        # Check if project exists
        project = next((p for p in projects_controller.data if p._id == args["project_id"]), None)
        if not project:
            print(f"Error: Project with ID {args['project_id']} not found.")
            return None
        
        # Check if user exists
        user = next((u for u in users_controller.data if u._id == args["assigned_to_id"]), None)
        if not user:
            print(f"Error: User with ID {args['assigned_to_id']} not found.")
            return None
        
        # Create task
        task = Task(
            project_id=args["project_id"],
            title=args["title"],
            assigned_to_id=args["assigned_to_id"]
        )
        self.data.append(task)
        print(f"Task '{task.title}' added successfully with ID: {task._id}.")
        return task


    # Get task by ID
    def get_task(self, args, users_controller, projects_controller):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        # Task not found
        if not task:
            print(f"Error: Task with ID {args['id']} not found.")
            return None
        
        # Look up project name
        project = next((p for p in projects_controller.data if p._id == task.project_id), None)
        project_name = project.title if project else "Unknown"
        
        # Look up assigned user
        user = next((u for u in users_controller.data if u._id == task.assigned_to_id), None)
        assigned_to = user.name if user else "Unknown"
        
        # Task found
        print(f"ID: {task._id}, Title: {task.title}, Project: {project_name}, Assigned to: {assigned_to}, Status: {task.status}")
        return task


    # List tasks
    def list_tasks(self, users_controller, projects_controller):
        for task in self.data:
            # Look up project name
            project = next((p for p in projects_controller.data if p._id == task.project_id), None)
            project_name = project.title if project else "Unknown"
            
            # Look up assigned user
            user = next((u for u in users_controller.data if u._id == task.assigned_to_id), None)
            assigned_to = user.name if user else "Unknown"
            
            print(f"ID: {task._id}, Title: {task.title}, Project: {project_name}, Assigned to: {assigned_to}, Status: {task.status}")


    # Update task
    def update_task(self, args):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        if not task:
            print(f"Error: Task with ID {args['id']} not found.")
            return None
        
        # Update fields if provided
        if "title" in args:
            task.title = args["title"]
        if "assigned_to_id" in args:
            task.assigned_to_id = args["assigned_to_id"]
        if "status" in args:
            task.status = args["status"]
        
        print(f"Task '{task.title}' updated successfully.")
        return task
    

    # Delete task
    def delete_task(self, args):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        # Check if task exists
        if not task:
            print(f"Error: Task with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete task '{task.title}' (ID: {task._id})? (y/n): ")
        if confirm.lower() != "y":
            print("Delete cancelled.")
            return None
        
        # If confirmed, delete the task
        self.data.remove(task)
        print(f"Task '{task.title}' deleted successfully.")
        return task