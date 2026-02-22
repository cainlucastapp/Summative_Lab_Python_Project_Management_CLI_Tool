# lib/controllers/projects_controller.py

# Requires
from lib.models.project import Project
from lib.utils import storage
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime

# Console instance
console = Console()


class ProjectsController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []


    # Load data
    def __enter__(self):
        self.data = [Project.from_dict(project) for project in storage.load_data(self.file_path)]
        return self
 

    # Save data
    def __exit__(self, exc_type, exc_value, ex_tb):
        storage.save_data(self.file_path, [project.to_dict() for project in self.data])
    

    # Validate title
    @staticmethod
    def _validate_title(title):
        # Check not empty
        if not title.strip():
            console.print("[red]✗ Error:[/red] Title cannot be empty.")
            return False
        
        return True


    # Validate description
    @staticmethod
    def _validate_description(description):
        # Check not empty
        if not description.strip():
            console.print("[red]✗ Error:[/red] Description cannot be empty.")
            return False
        
        return True


    # Validate date
    @staticmethod
    def _validate_date(due_date):
        # Check not empty
        if not due_date.strip():
            console.print("[red]✗ Error:[/red] Due date cannot be empty.")
            return False
        
        # Check format MM-DD-YYYY
        try:
            parsed_date = datetime.strptime(due_date, "%m-%d-%Y")
        except ValueError:
            console.print("[red]✗ Error:[/red] Due date must be in MM-DD-YYYY format.")
            return False
        
        # Check date is in the future
        if parsed_date.date() < datetime.today().date():
            console.print("[red]✗ Error:[/red] Due date must be in the future.")
            return False
        
        return True


    # Validate status
    @staticmethod
    def _validate_status(status):
        # Check not empty
        if not status.strip():
            console.print("[red]✗ Error:[/red] Status cannot be empty.")
            return False
        
        # Check valid values
        if status.lower() not in ["active", "completed"]:
            console.print("[red]✗ Error:[/red] Status must be 'active' or 'completed'.")
            return False
        
        return True


    # Add project
    def add_project(self, args, users_controller):
        # Validate title
        if not self._validate_title(args["title"]):
            return None
        
        # Validate description
        if not self._validate_description(args["description"]):
            return None
        
        # Validate due date
        if not self._validate_date(args["due_date"]):
            return None
        
        # Check if user exists
        user = next((u for u in users_controller.data if u._id == args["assigned_to_id"]), None)
        if not user:
            console.print(f"[red]✗ Error:[/red] User with ID {args['assigned_to_id']} not found.")
            return None
        
        # Create project
        project = Project(
            assigned_to_id=args["assigned_to_id"],
            title=args["title"],
            description=args["description"],
            due_date=args["due_date"]
        )
        self.data.append(project)
        console.print(f"[green]✓ Success:[/green] Project '{project.title}' added successfully with ID: {project._id}.")
        return project

    # Get project by ID with owner and tasks
    def get_project(self, args, users_controller=None, tasks_controller=None):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        # Project not found
        if not project:
            console.print(f"[red]✗ Error:[/red] Project with ID {args['id']} not found.")
            return None
        
        # Look up assigned user
        user = None
        if users_controller:
            user = next((u for u in users_controller.data if u._id == project.assigned_to_id), None)
        
        # Format status with color
        status_color = "orange1" if project.status == "active" else "blue"
        
        # Project header
        console.print(f"\n[bold green]Project: {project.title}[/bold green]")
        console.print(f"Description: {project.description}")
        console.print(f"Status: [{status_color}]{project.status}[/{status_color}] | Due: {project.due_date}")
        console.print(f"Assigned to: {user.name if user else 'Unknown'}")
        console.print(f"ID: {project._id}\n")
        console.rule()
        
        # If no tasks controller provided, just show project info
        if not tasks_controller:
            return project
        
        # Find tasks for this project
        project_tasks = [t for t in tasks_controller.data if t.project_id == project._id]
        
        if not project_tasks:
            console.print("[yellow]⚠ Warning:[/yellow] No tasks found for this project.")
            return project
        
        # Create task table
        console.print("\n[bold]Tasks:[/bold]\n")
        task_table = Table(box=box.SIMPLE, show_header=True)
        task_table.add_column("ID", style="cyan", justify="center")
        task_table.add_column("Title", style="white")
        task_table.add_column("Status", justify="center")
        
        for task in project_tasks:
            # Color-code status
            if task.status == "active":
                status_display = "[orange1]active[/orange1]"
            else:
                status_display = "[blue]completed[/blue]"
            
            task_table.add_row(task._id, task.title, status_display)
        
        console.print(task_table)
        console.rule()
        
        return project


    # List projects
    def list_projects(self, users_controller):
        # Check if there are any projects
        if not self.data:
            console.print("[yellow]⚠ Warning:[/yellow] No projects found.")
            return
        
        # Create table
        table = Table(title="All Projects", box=box.SIMPLE)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Title", style="white")
        table.add_column("Assigned To", style="white")
        table.add_column("Status", justify="center")
        table.add_column("Due Date", style="white", justify="center")
        
        # Add rows
        for project in self.data:
            # Look up assigned user
            user = next((u for u in users_controller.data if u._id == project.assigned_to_id), None)
            assigned_to = user.name if user else "Unknown"
            
            # Color-code status
            if project.status == "active":
                status_display = "[orange1]active[/orange1]"
            else:
                status_display = "[blue]completed[/blue]"
            
            table.add_row(project._id, project.title, assigned_to, status_display, project.due_date)
        
        console.print(table)


    # Update project
    def update_project(self, args):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        if not project:
            console.print(f"[red]✗ Error:[/red] Project with ID {args['id']} not found.")
            return None
        
        # Validate title if updating
        if "title" in args:
            if not self._validate_title(args["title"]):
                return None
        
        # Validate description if updating
        if "description" in args:
            if not self._validate_description(args["description"]):
                return None
        
        # Validate due date if updating
        if "due_date" in args:
            if not self._validate_date(args["due_date"]):
                return None
        
        # Validate status if updating
        if "status" in args:
            if not self._validate_status(args["status"]):
                return None
        
        # Update fields if provided
        if "title" in args:
            project.title = args["title"]
        if "description" in args:
            project.description = args["description"]
        if "due_date" in args:
            project.due_date = args["due_date"]
        if "status" in args:
            project.status = args["status"]
        
        console.print(f"[green]✓ Success:[/green] Project '{project.title}' updated successfully.")
        return project
    

    # Delete project
    def delete_project(self, args):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        # Check if project exists
        if not project:
            console.print(f"[red]✗ Error:[/red] Project with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete project '{project.title}' (ID: {project._id})? (y/n): ")
        if confirm.lower() != "y":
            console.print("[yellow]⚠ Warning:[/yellow] Delete cancelled.")
            return None
        
        # If confirmed, delete the project
        self.data.remove(project)
        console.print(f"[green]✓ Success:[/green] Project '{project.title}' deleted successfully.")
        return project