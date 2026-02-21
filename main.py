# main.py

# Requires
from lib.controllers.users_controller import UsersController
from lib.controllers.projects_controller import ProjectsController
from lib.controllers.tasks_controller import TasksController
from lib.utils.args import create_parser


def main():
    # File paths
    users_file = "data/users.json"
    projects_file = "data/projects.json"
    tasks_file = "data/tasks.json"
    
    # Create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Open controllers with context managers
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                
                # Route commands using match/case
                match args.command:
                    
                    # Add user
                    case "add-user":
                        users_controller.add_user({"name": args.name, "email": args.email})
                    
                    # List users
                    case "list-users":
                        users_controller.list_users()
                    
                    # Get user
                    case "get-user":
                        users_controller.get_user({"id": args.id})
                    
                    # Update user
                    case "update-user":
                        update_args = {"id": args.id}
                        if args.name:
                            update_args["name"] = args.name
                        if args.email:
                            update_args["email"] = args.email
                        users_controller.update_user(update_args)
                    
                    # Delete user
                    case "delete-user":
                        users_controller.delete_user({"id": args.id})
                    
                    # Add project
                    case "add-project":
                        projects_controller.add_project({
                            "assigned_to_id": args.assigned_to_id,
                            "title": args.title,
                            "description": args.description,
                            "due_date": args.due_date
                        }, users_controller)
                    
                    # List projects
                    case "list-projects":
                        projects_controller.list_projects(users_controller)
                    
                    # Get project
                    case "get-project":
                        projects_controller.get_project({"id": args.id}, users_controller)
                    
                    # Update project
                    case "update-project":
                        update_args = {"id": args.id}
                        if args.title:
                            update_args["title"] = args.title
                        if args.description:
                            update_args["description"] = args.description
                        if args.due_date:
                            update_args["due_date"] = args.due_date
                        if args.status:
                            update_args["status"] = args.status
                        projects_controller.update_project(update_args)
                    
                    # Delete project
                    case "delete-project":
                        projects_controller.delete_project({"id": args.id})
                    
                    # Add task
                    case "add-task":
                        tasks_controller.add_task({
                            "project_id": args.project_id,
                            "title": args.title,
                            "assigned_to_id": args.assigned_to_id
                        }, users_controller, projects_controller)
                    
                    # List tasks
                    case "list-tasks":
                        tasks_controller.list_tasks(users_controller, projects_controller)
                    
                    # Get task
                    case "get-task":
                        tasks_controller.get_task({"id": args.id}, users_controller, projects_controller)
                    
                    # Update task
                    case "update-task":
                        update_args = {"id": args.id}
                        if args.title:
                            update_args["title"] = args.title
                        if args.assigned_to_id:
                            update_args["assigned_to_id"] = args.assigned_to_id
                        if args.status:
                            update_args["status"] = args.status
                        tasks_controller.update_task(update_args)
                    
                    # Delete task
                    case "delete-task":
                        tasks_controller.delete_task({"id": args.id})
                    
                    # Unknown command
                    case _:
                        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()