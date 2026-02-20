# lib/controllers/users_controller.py

#Requires
from lib.models.user import User
from lib.utils import storage



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
    
    
    def add_user(self, args):
        if any(u.email == args["email"] for u in self.data):
            print(f"Error: User with email {args['email']} already exists.")
            return
        
        user = User(name=args["name"], email=args["email"])
        self.data.append(user)
        print(f"User {user.name} added successfully with ID: {user._id}.")
        
        return user