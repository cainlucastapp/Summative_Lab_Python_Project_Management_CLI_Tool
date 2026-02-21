# lib/controllers/users_controller.py

# Requires
from lib.models.user import User
from lib.utils import storage
import re


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
            print("Error: Name cannot be empty.")
            return False
        
        # Check format: letters, spaces, periods, hyphens, apostrophes only
        if not re.fullmatch(r"[A-Za-z][A-Za-z\s'\.\-]*", name):
            print("Error: Name can only contain letters, spaces, periods, hyphens, and apostrophes.")
            return False
        
        return True


    # Validate email
    @staticmethod
    def _validate_email(email):
        # Check not empty
        if not email.strip():
            print("Error: Email cannot be empty.")
            return False
        
        # Check format
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            print("Error: Invalid email format.")
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
            print(f"Error: User with email {args['email']} already exists.")
            return None
        
        # Create user
        user = User(name=args["name"], email=args["email"])
        self.data.append(user)
        print(f"User {user.name} added successfully with ID: {user._id}.")
        return user


    # Get user by ID
    def get_user(self, args):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        # User not found
        if not user:
            print(f"Error: User with ID {args['id']} not found.")
            return None
        
        # User found
        print(f"ID: {user._id}, Name: {user.name}, Email: {user.email}")
        return user


    # List users
    def list_users(self):
        # Check if there are any users
        if not self.data:
            print("No users found.")
            return
        
        for user in self.data:
            print(f"ID: {user._id}, Name: {user.name}, Email: {user.email}")


    # Update user
    def update_user(self, args):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        if not user:
            print(f"Error: User with ID {args['id']} not found.")
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
                    print(f"Error: Email {args['email']} is already in use.")
                    return None
        
        # Update fields if provided
        if "name" in args:
            user.name = args["name"]
        if "email" in args:
            user.email = args["email"]
        
        print(f"User {user.name} updated successfully.")
        return user
    

    # Delete user
    def delete_user(self, args):
        user = next((u for u in self.data if u._id == args["id"]), None)
        
        # Check if user exists
        if not user:
            print(f"Error: User with ID {args['id']} not found.")
            return None
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete user {user.name} (ID: {user._id})? (y/n): ")
        if confirm.lower() != "y":
            print("Delete cancelled.")
            return None
        
        # If confirmed, delete the user
        self.data.remove(user)
        print(f"User {user.name} deleted successfully.")
        return user