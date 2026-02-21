# lib/utils/args.py

# Requires
import argparse


def create_parser():
    # Create the main parser
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup user parsers
    setup_user_parsers(subparsers)
    
    # Setup project parsers
    setup_project_parsers(subparsers)
    
    # Setup task parsers
    setup_task_parsers(subparsers)
    
    return parser


def setup_user_parsers(subparsers):
    # Add user
    parser_add_user = subparsers.add_parser("add-user", help="Add a new user")
    parser_add_user.add_argument("--name", required=True, help="User name")
    parser_add_user.add_argument("--email", required=True, help="User email")
    
    # List users
    parser_list_users = subparsers.add_parser("list-users", help="List all users")
    
    # Get user
    parser_get_user = subparsers.add_parser("get-user", help="Get user by ID")
    parser_get_user.add_argument("--id", required=True, help="User ID")
    
    # Update user
    parser_update_user = subparsers.add_parser("update-user", help="Update an existing user")
    parser_update_user.add_argument("--id", required=True, help="User ID")
    parser_update_user.add_argument("--name", help="New user name")
    parser_update_user.add_argument("--email", help="New user email")
    
    # Delete user
    parser_delete_user = subparsers.add_parser("delete-user", help="Delete a user")
    parser_delete_user.add_argument("--id", required=True, help="User ID")


def setup_project_parsers(subparsers):
    # Add project
    parser_add_project = subparsers.add_parser("add-project", help="Add a new project")
    parser_add_project.add_argument("--assigned-to-id", required=True, help="User ID to assign project to")
    parser_add_project.add_argument("--title", required=True, help="Project title")
    parser_add_project.add_argument("--description", required=True, help="Project description")
    parser_add_project.add_argument("--due-date", required=True, help="Due date (MM-DD-YYYY)")
    
    # List projects
    parser_list_projects = subparsers.add_parser("list-projects", help="List all projects")
    
    # Get project
    parser_get_project = subparsers.add_parser("get-project", help="Get project by ID")
    parser_get_project.add_argument("--id", required=True, help="Project ID")
    
    # Update project
    parser_update_project = subparsers.add_parser("update-project", help="Update an existing project")
    parser_update_project.add_argument("--id", required=True, help="Project ID")
    parser_update_project.add_argument("--title", help="New project title")
    parser_update_project.add_argument("--description", help="New project description")
    parser_update_project.add_argument("--due-date", help="New due date (MM-DD-YYYY)")
    parser_update_project.add_argument("--status", help="New status (active/completed)")
    
    # Delete project
    parser_delete_project = subparsers.add_parser("delete-project", help="Delete a project")
    parser_delete_project.add_argument("--id", required=True, help="Project ID")


def setup_task_parsers(subparsers):
    # Add task
    parser_add_task = subparsers.add_parser("add-task", help="Add a new task")
    parser_add_task.add_argument("--project-id", required=True, help="Project ID")
    parser_add_task.add_argument("--title", required=True, help="Task title")
    
    # List tasks
    parser_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks")
    
    # Get task
    parser_get_task = subparsers.add_parser("get-task", help="Get task by ID")
    parser_get_task.add_argument("--id", required=True, help="Task ID")
    
    # Update task
    parser_update_task = subparsers.add_parser("update-task", help="Update an existing task")
    parser_update_task.add_argument("--id", required=True, help="Task ID")
    parser_update_task.add_argument("--title", help="New task title")
    parser_update_task.add_argument("--status", help="New status (active/completed)")
    
    # Delete task
    parser_delete_task = subparsers.add_parser("delete-task", help="Delete a task")
    parser_delete_task.add_argument("--id", required=True, help="Task ID")