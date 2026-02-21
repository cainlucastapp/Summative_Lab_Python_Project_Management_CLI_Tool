# READ ME COMMING SOON

## Installation

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
python main.py add-task --project-id "PROJECT_ID" --title "Task Title" --assigned-to-id "USER_ID"

# List all tasks
python main.py list-tasks

# Get task by ID
python main.py get-task --id "TASK_ID"

# Update task
python main.py update-task --id "TASK_ID" --title "New Title" --assigned-to-id "NEW_USER_ID" --status "completed"

# Delete task
python main.py delete-task --id "TASK_ID"
```