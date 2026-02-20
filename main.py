# main.py

from lib.utils import storage

def main():
    print("[START]")

    user_file = storage.get_settings("user_file", "data/user_data.json")
    project_file = storage.get_settings("project_file", "data/project_data.json")
    task_file = storage.get_settings("task_file", "data/task_data.json")
    
    print(f"User file: {user_file}")
    print(f"Project file: {project_file}")
    print(f"Task file: {task_file}")
    

    print("[END]")


if __name__ == "__main__":
    main()