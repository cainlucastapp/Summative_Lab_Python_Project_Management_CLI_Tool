# lib/controllers/projects_controller.py

# Requires
from lib.models.project import Project
from lib.utils import storage
from datetime import datetime


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
            print("Error: Title cannot be empty.")
            return False
        
        return True


    # Validate description
    @staticmethod
    def _validate_description(description):
        # Check not empty
        if not description.strip():
            print("Error: Description cannot be empty.")
            return False
        
        return True


    # Validate date
    @staticmethod
    def _validate_date(due_date):
        # Check not empty
        if not due_date.strip():
            print("Error: Due date cannot be empty.")
            return False
        
        # Check format MM-DD-YYYY
        try:
            parsed_date = datetime.strptime(due_date, "%m-%d-%Y")
        except ValueError:
            print("Error: Due date must be in MM-DD-YYYY format.")
            return False
        
        # Check date is in the future
        if parsed_date.date() < datetime.today().date():
            print("Error: Due date must be in the future.")
            return False
        
        return True


    # Validate status
    @staticmethod
    def _validate_status(status):
        # Check not empty
        if not status.strip():
            print("Error: Status cannot be empty.")
            return False
        
        # Check valid values
        if status.lower() not in ["active", "completed"]:
            print("Error: Status must be 'active' or 'completed'.")
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
            print(f"Error: User with ID {args['assigned_to_id']} not found.")
            return None
        
        # Create project
        project = Project(
            assigned_to_id=args["assigned_to_id"],
            title=args["title"],
            description=args["description"],
            due_date=args["due_date"]
        )
        self.data.append(project)
        print(f"Project '{project.title}' added successfully with ID: {project._id}.")
        return project


    # Get project by ID
    def get_project(self, args, users_controller):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        # Project not found
        if not project:
            print(f"Error: Project with ID {args['id']} not found.")
            return None
        
        # Look up assigned user
        user = next((u for u in users_controller.data if u._id == project.assigned_to_id), None)
        assigned_to = user.name if user else "Unknown"
        
        # Project found
        print(f"ID: {project._id}, Title: {project.title}, Assigned to: {assigned_to}, Status: {project.status}, Due: {project.due_date}")
        return project


    # List projects
    def list_projects(self, users_controller):
        # Check if there are any projects
        if not self.data:
            print("No projects found.")
            return
        
        for project in self.data:
            # Look up assigned user
            user = next((u for u in users_controller.data if u._id == project.assigned_to_id), None)
            assigned_to = user.name if user else "Unknown"
            
            print(f"ID: {project._id}, Title: {project.title}, Assigned to: {assigned_to}, Status: {project.status}, Due: {project.due_date}")


    # Update project
    def update_project(self, args):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        if not project:
            print(f"Error: Project with ID {args['id']} not found.")
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
        
        print(f"Project '{project.title}' updated successfully.")
        return project
    

    # Delete project
    def delete_project(self, args):
        project = next((p for p in self.data if p._id == args["id"]), None)
        
        # Check if project exists
        if not project:
            print(f"Error: Project with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete project '{project.title}' (ID: {project._id})? (y/n): ")
        if confirm.lower() != "y":
            print("Delete cancelled.")
            return None
        
        # If confirmed, delete the project
        self.data.remove(project)
        print(f"Project '{project.title}' deleted successfully.")
        return project