# Project Management CLI

A command-line interface tool for managing users, projects, and tasks. Built with Python, this CLI tool provides a simple and efficient way to organize project workflows with persistent data storage and rich formatted output.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-cli
```

2. Install dependencies using Pipenv:
```bash
python -m pipenv install
```

3. Activate the virtual environment:
```bash
python -m pipenv shell
```

4. Run the application:
```bash
python main.py --help
```

## Tech Stack

- **Python 3.13** - Core programming language
- **Rich** - Terminal formatting and colored output
- **pytest** - Testing framework
- **JSON** - Data persistence
- **argparse** - Command-line argument parsing
- **uuid** - Unique ID generation


## Project Structure
```
project-management-cli/
├── lib/
│   ├── models/          # Data models (User, Project, Task)
│   ├── controllers/     # Business logic and CRUD operations
│   └── utils/           # Utilities (storage, args, helpers)
├── tests/               # Test suite
├── data/                # JSON data storage
├── main.py              # Entry point
└── Pipfile              # Dependency management
```

## Available Commands

### User Commands
```bash
# Add a new user
python main.py add-user --name "Alice Smith" --email "alice@example.com"

# List all users
python main.py list-users

# Get user by ID
python main.py get-user --id "USER_ID"

# Update user
python main.py update-user --id "USER_ID" --name "New Name" --email "new@example.com"

# Delete user
python main.py delete-user --id "USER_ID"
```

### Project Commands
```bash
# Add a new project
python main.py add-project --assigned-to-id "USER_ID" --title "Project Title" --description "Project description" --due-date "12-31-2026"

# List all projects
python main.py list-projects

# Get project by ID
python main.py get-project --id "PROJECT_ID"

# Update project
python main.py update-project --id "PROJECT_ID" --title "New Title" --description "New description" --due-date "01-15-2027" --status "completed"

# Delete project
python main.py delete-project --id "PROJECT_ID"
```

### Task Commands
```bash
# Add a new task
python main.py add-task --project-id "PROJECT_ID" --title "Task Title"

# List all tasks
python main.py list-tasks

# Get task by ID
python main.py get-task --id "TASK_ID"

# Update task
python main.py update-task --id "TASK_ID" --title "New Title" --status "completed"

# Delete task
python main.py delete-task --id "TASK_ID"
```

## Testing Commands
```bash
# Run all tests with verbose output
python -m pytest -v

# Run all model tests
python -m pytest tests/test_models.py -v

# Run all user controller tests
python -m pytest tests/test_users_controller.py -v

# Run all project controller tests
python -m pytest tests/test_projects_controller.py -v

# Run all task controller tests
python -m pytest tests/test_tasks_controller.py -v
```