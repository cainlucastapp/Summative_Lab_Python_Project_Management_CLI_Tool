# main.py
# Run with pipenv run python main.py

#Requires
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
    
    #users_controller = UsersController(users_file)
    #users_controller.data = storage.load_data(users_file)
    #user = users_controller.add_user({ "name": "George", "email": "george@email.com"})
    
    with UsersController(users_file) as users_controller:
        #user = users_controller.add_user({ "name": "Bobo", "email": "bobo@email.com"})
        #users_controller.list_users()
        #users_controller.update_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd","name": "Bobby","email": "bobby@email.com"})
        #users_controller.get_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd"})
        #users_controller.delete_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd"})
        
        users_controller.list_users()

    #print(user)
    
    #storage.save_data(users_file, [ user.to_dict() for user in users_controller.data ])
    
    print("[END]")


if __name__ == "__main__":
    main()