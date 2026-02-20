# main.py

from lib.utils import storage
from lib.controllers.users_controller import UsersController


def main():
    print("[START]")

    users_file = storage.get_settings("user_file", "data/user_data.json")
    project_file = storage.get_settings("project_file", "data/project_data.json")
    task_file = storage.get_settings("task_file", "data/task_data.json")
    
    #print(f"User file: {users_file}")
    #print(f"Project file: {project_file}")
    #print(f"Task file: {task_file}")
    
    users_controller = UsersController(users_file)
    users_controller.data = storage.load_data(users_file)
    user = users_controller.add_user({ "name": "George", "email": "george@email.com"})
    
    print(user)
    
    storage.save_data(users_file, [ user.to_dict() for user in users_controller.data ])
    
    print("[END]")


if __name__ == "__main__":
    main()