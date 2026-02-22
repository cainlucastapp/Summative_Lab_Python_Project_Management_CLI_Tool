# lib/controllers/tasks_controller.py

# Requires
from lib.models.task import Task
from lib.utils import storage
from rich.console import Console
from rich.table import Table
from rich import box

# Console instance
console = Console()


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
    

    # Validate title
    @staticmethod
    def _validate_title(title):
        # Check not empty
        if not title.strip():
            console.print("─" * 60, style="dim")
            console.print("[red]✗ Error:[/red] Title cannot be empty.")
            console.print("─" * 60, style="dim")
            return False
        
        return True


    # Validate status
    @staticmethod
    def _validate_status(status):
        # Check not empty
        if not status.strip():
            console.print("─" * 60, style="dim")
            console.print("[red]✗ Error:[/red] Status cannot be empty.")
            console.print("─" * 60, style="dim")
            return False
        
        # Check valid values
        if status.lower() not in ["active", "completed"]:
            console.print("[red]✗ Error:[/red] Status must be 'active' or 'completed'.")
            return False
        
        return True


    # Add task
    def add_task(self, args, projects_controller):
        # Validate title
        if not self._validate_title(args["title"]):
            return None
        
        # Check if project exists
        project = next((p for p in projects_controller.data if p._id == args["project_id"]), None)
        if not project:
            console.print(f"[red]✗ Error:[/red] Project with ID {args['project_id']} not found.")
            return None
        
        # Create task
        task = Task(
            project_id=args["project_id"],
            title=args["title"]
        )
        self.data.append(task)
        console.print(f"[green]✓ Success:[/green] Task '{task.title}' added successfully with ID: {task._id}.")
        return task


    # Get task by ID
    def get_task(self, args, projects_controller):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        # Task not found
        if not task:
            console.print(f"[red]✗ Error:[/red] Task with ID {args['id']} not found.")
            return None
        
        # Look up project name
        project = next((p for p in projects_controller.data if p._id == task.project_id), None)
        project_name = project.title if project else "Unknown"
        
        # Format status with color
        status_color = "orange1" if task.status == "active" else "blue"
        
        # Task found
        console.print(f"ID: {task._id}, Title: {task.title}, Project: {project_name}, Status: [{status_color}]{task.status}[/{status_color}]")
        return task


    # List tasks
    def list_tasks(self, projects_controller):
        # Check if there are any tasks
        if not self.data:
            console.print("[yellow]⚠ Warning:[/yellow] No tasks found.")
            return
        
        # Create table
        table = Table(title="All Tasks", box=box.SIMPLE)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Title", style="white")
        table.add_column("Project", style="white")
        table.add_column("Status", justify="center")
        
        # Add rows
        for task in self.data:
            # Look up project name
            project = next((p for p in projects_controller.data if p._id == task.project_id), None)
            project_name = project.title if project else "Unknown"
            
            # Color-code status
            if task.status == "active":
                status_display = "[orange1]active[/orange1]"
            else:
                status_display = "[blue]completed[/blue]"
            
            table.add_row(task._id, task.title, project_name, status_display)
        
        console.print(table)


    # Update task
    def update_task(self, args):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        if not task:
            console.print(f"[red]✗ Error:[/red] Task with ID {args['id']} not found.")
            return None
        
        # Validate title if updating
        if "title" in args:
            if not self._validate_title(args["title"]):
                return None
        
        # Validate status if updating
        if "status" in args:
            if not self._validate_status(args["status"]):
                return None
        
        # Update fields if provided
        if "title" in args:
            task.title = args["title"]
        if "status" in args:
            task.status = args["status"]
        
        console.print(f"[green]✓ Success:[/green] Task '{task.title}' updated successfully.")
        return task
    

    # Delete task
    def delete_task(self, args):
        task = next((t for t in self.data if t._id == args["id"]), None)
        
        # Check if task exists
        if not task:
            console.print(f"[red]✗ Error:[/red] Task with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete task '{task.title}' (ID: {task._id})? (y/n): ")
        if confirm.lower() != "y":
            console.print("[yellow]⚠ Warning:[/yellow] Delete cancelled.")
            return None
        
        # If confirmed, delete the task
        self.data.remove(task)
        console.print(f"[green]✓ Success:[/green] Task '{task.title}' deleted successfully.")
        return task