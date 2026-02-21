# lib/controllers/projects_controller.py

# Requires
from lib.models.project import Project
from lib.utils import storage


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
    

    # Add project
    def add_project(self, args, users_controller):
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