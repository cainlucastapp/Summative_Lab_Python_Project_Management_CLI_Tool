# main.py
# Run with pipenv run python main.py

#Requires
from lib.utils import storage
from lib.controllers.users_controller import UsersController
from lib.controllers.projects_controller import ProjectsController
from lib.controllers.tasks_controller import TasksController

def main():
    print("[START]")

    user_file = storage.get_settings("user_file", "data/users.json")
    project_file = storage.get_settings("project_file", "data/projects.json")
    task_file = storage.get_settings("task_file", "data/tasks.json")
    
    #print(f"User file: {users_file}")
    #print(f"Project file: {project_file}")
    #print(f"Task file: {task_file}")
    
    #users_controller = UsersController(users_file)
    #users_controller.data = storage.load_data(users_file)
    #user = users_controller.add_user({ "name": "George", "email": "george@email.com"})
    
    with UsersController(user_file) as users_controller:
        with ProjectsController(project_file) as projects_controller:
            with TasksController(task_file) as tasks_controller:
                    
                # Add project
                #projects_controller.add_project({"assigned_to_id": "92b50a86-d644-4018-b5ae-ab194d6f0480", "title": "Website Redesign", "description": "Redesign company website", "due_date": "12-31-2026"}, users_controller)
            
                # List all projects
                #projects_controller.list_projects(users_controller)
            
                # Get project by ID
                #projects_controller.get_project({"id": "a5847a3a-8def-40d4-8e31-fc9b9422cd83"}, users_controller)
                
                # Update project
                #projects_controller.update_project({"id": "a5847a3a-8def-40d4-8e31-fc9b9422cd83", "title": "New Title", "status": "completed"})
                
                # Delete project
                #projects_controller.delete_project({"id": "a5847a3a-8def-40d4-8e31-fc9b9422cd83"})
                
                #user = users_controller.add_user({ "name": "Bobo", "email": "bobo@email.com"})
                #users_controller.list_users()
                #users_controller.update_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd","name": "Bobby","email": "bobby@email.com"})
                #users_controller.get_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd"})
                #users_controller.delete_user({"id": "87cc7736-2456-4390-b24b-5988ed3df6bd"})
                
                #users_controller.list_users()
                
                # Add task
                #tasks_controller.add_task({"project_id": "13a5f26b-00f9-47cf-9681-0ad2b5038835", "title": "Design homepage mockup", "assigned_to_id": "92b50a86-d644-4018-b5ae-ab194d6f0480"}, users_controller, projects_controller)
                
                # List all tasks
                #tasks_controller.list_tasks(users_controller, projects_controller)
                
                # Get task by ID
                #tasks_controller.get_task({"id": "97a653c6-d10f-4142-8574-2a6a1293e1d0"}, users_controller, projects_controller)
                
                # Update task
                #tasks_controller.update_task({"id": "97a653c6-d10f-4142-8574-2a6a1293e1d0", "title": "New Title", "status": "completed"})
                
                # Delete task
                #tasks_controller.delete_task({"id": "97a653c6-d10f-4142-8574-2a6a1293e1d0"})
                
            
            

                #print(user)
        
                #storage.save_data(users_file, [ user.to_dict() for user in users_controller.data ])
        
                print("[END]")


if __name__ == "__main__":
    main()