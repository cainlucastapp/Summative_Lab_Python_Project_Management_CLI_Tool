# lib/controllers/users_controller.py

# Requires
from lib.models.user import User
from lib.utils import storage
from rich.console import Console
from rich.table import Table
from rich import box
import re

# Console instance
console = Console()


class UsersController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []


    # Load data
    def __enter__(self):
        self.data = [User.from_dict(user) for user in storage.load_data(self.file_path)]
        return self
 

    # Save data
    def __exit__(self, exc_type, exc_value, ex_tb):
        storage.save_data(self.file_path, [user.to_dict() for user in self.data])
    

    # Validate name
    @staticmethod
    def _validate_name(name):
        # Check not empty
        if not name.strip():
            console.print("[red]✗ Error:[/red] Name cannot be empty.")
            return False
        
        # Check format: letters, spaces, periods, hyphens, apostrophes only
        if not re.fullmatch(r"[A-Za-z][A-Za-z\s'\.\-]*", name):
            console.print("[red]✗ Error:[/red] Name can only contain letters, spaces, periods, hyphens, and apostrophes.")
            return False
        
        return True


    # Validate email
    @staticmethod
    def _validate_email(email):
        # Check not empty
        if not email.strip():
            console.print("[red]✗ Error:[/red] Email cannot be empty.")
            return False
        
        # Check format
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            console.print("[red]✗ Error:[/red] Invalid email format.")
            return False
        
        return True


    # Add user
    def add_user(self, args):
        # Validate name
        if not self._validate_name(args["name"]):
            return None
        
        # Validate email
        if not self._validate_email(args["email"]):
            return None
        
        # Check for duplicate email
        if any(u.email == args["email"] for u in self.data):
            console.print(f"[red]✗ Error:[/red] User with email {args['email']} already exists.")
            return None
        
        # Create user
        user = User(name=args["name"], email=args["email"])
        self.data.append(user)
        console.print(f"[green]✓ Success:[/green] User {user.name} added successfully with ID: {user._id}.")
        return user


    # Get user by ID with all projects and tasks 
    def get_user(self, args, projects_controller=None, tasks_controller=None):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        # User not found
        if not user:
            console.print(f"[red]✗ Error:[/red] User with ID {args['id']} not found.")
            return None
        
        # User header
        console.print(f"\n[bold cyan]User: {user.name}[/bold cyan]")
        console.print(f"Email: {user.email}")
        console.print(f"ID: {user._id}\n")
        console.rule()
        
        # If no controllers provided, just show user info
        if not projects_controller or not tasks_controller:
            return user
        
        # Find user's projects
        user_projects = [p for p in projects_controller.data if p.assigned_to_id == user._id]
        
        if not user_projects:
            console.print("[yellow]⚠ Warning:[/yellow] No projects found for this user.")
            return user
        
        # Display each project with its tasks
        for project in user_projects:
            # Format status with color
            status_color = "orange1" if project.status == "active" else "blue"
            
            console.print(f"\n[bold green]Project: {project.title}[/bold green]")
            console.print(f"Description: {project.description}")
            console.print(f"Status: [{status_color}]{project.status}[/{status_color}] | Due: {project.due_date}")
            console.print(f"ID: {project._id}\n")
            
            # Find tasks for this project
            project_tasks = [t for t in tasks_controller.data if t.project_id == project._id]
            
            if not project_tasks:
                console.print("  [yellow]No tasks for this project[/yellow]")
            else:
                # Create task table
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
        
        return user


    # List users
    def list_users(self):
        # Check if there are any users
        if not self.data:
            console.print("[yellow]⚠ Warning:[/yellow] No users found.")
            return
        
        # Create table
        table = Table(title="All Users", box=box.SIMPLE)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="white")
        table.add_column("Email", style="white")
        
        # Add rows
        for user in self.data:
            table.add_row(user._id, user.name, user.email)
        
        console.print(table)


    # Update user
    def update_user(self, args):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        if not user:
            console.print(f"[red]✗ Error:[/red] User with ID {args['id']} not found.")
            return None
        
        # Validate name if updating
        if "name" in args:
            if not self._validate_name(args["name"]):
                return None
        
        # Validate email if updating
        if "email" in args:
            if not self._validate_email(args["email"]):
                return None
            
            # Check for duplicate email if updating email
            if args["email"] != user.email:
                if any(u.email == args["email"] for u in self.data):
                    console.print(f"[red]✗ Error:[/red] Email {args['email']} is already in use.")
                    return None
        
        # Update fields if provided
        if "name" in args:
            user.name = args["name"]
        if "email" in args:
            user.email = args["email"]
        
        console.print(f"[green]✓ Success:[/green] User {user.name} updated successfully.")
        return user
    

    # Delete user
    def delete_user(self, args):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        # Check if user exists
        if not user:
            console.print(f"[red]✗ Error:[/red] User with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete user {user.name} (ID: {user._id})? (y/n): ")
        if confirm.lower() != "y":
            console.print("[yellow]⚠ Warning:[/yellow] Delete cancelled.")
            return None
        
        # If confirmed, delete the user
        self.data.remove(user)
        console.print(f"[green]✓ Success:[/green] User {user.name} deleted successfully.")
        return user