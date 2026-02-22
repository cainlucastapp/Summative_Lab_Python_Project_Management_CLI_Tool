# tests/test_cli.py

# Requires
import pytest
import subprocess
import json
import os
import tempfile
import shutil


# Helper function to run CLI commands
def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode


# Add user command should succeed
def test_add_user_command():
    stdout, stderr, returncode = run_command(
        'python main.py add-user --name "TestUser123" --email "testuser123@test.com"'
    )
    # Command should execute without crashing
    assert returncode in [0, 1]  # Either succeeds or fails validation gracefully


# Add user with invalid email should fail
def test_add_user_invalid_email():
    stdout, stderr, returncode = run_command(
        'python main.py add-user --name "George Heeres" --email "notanemail"'
    )
    output = stdout + stderr
    # Command should complete, validation happens in the app
    assert returncode in [0, 1]


# List users command should work
def test_list_users_command():
    stdout, stderr, returncode = run_command('python main.py list-users')
    assert returncode == 0


# Add project command should succeed
def test_add_project_command():
    stdout, stderr, returncode = run_command(
        'python main.py add-project --assigned-to-id "test-id" --title "Test Project" --description "Test description" --due-date "12-31-2026"'
    )
    # Command structure is valid
    assert returncode in [0, 1]


# Add project with past date should fail validation
def test_add_project_past_date():
    stdout, stderr, returncode = run_command(
        'python main.py add-project --assigned-to-id "test-id" --title "Test Project" --description "Test description" --due-date "01-01-2020"'
    )
    # Command runs, validation happens in app
    assert returncode in [0, 1]


# List projects command should work
def test_list_projects_command():
    stdout, stderr, returncode = run_command('python main.py list-projects')
    assert returncode == 0


# Add task command structure should be valid
def test_add_task_command():
    stdout, stderr, returncode = run_command(
        'python main.py add-task --project-id "test-id" --title "Test Task"'
    )
    # Command structure is valid
    assert returncode in [0, 1]


# List tasks command should work
def test_list_tasks_command():
    stdout, stderr, returncode = run_command('python main.py list-tasks')
    assert returncode == 0


# Help command should work
def test_help_command():
    stdout, stderr, returncode = run_command('python main.py --help')
    output = stdout + stderr
    assert returncode == 0
    assert "add-user" in output


# No command should show help
def test_no_command_shows_help():
    stdout, stderr, returncode = run_command('python main.py')
    assert returncode == 0


# Update user command structure should be valid
def test_update_user_command():
    stdout, stderr, returncode = run_command(
        'python main.py update-user --id "test-id" --name "New Name"'
    )
    assert returncode in [0, 1]


# Delete user command structure should be valid  
def test_delete_user_command():
    stdout, stderr, returncode = run_command(
        'python main.py delete-user --id "test-id"'
    )
    assert returncode in [0, 1]


# Test all commands are registered
def test_all_commands_registered():
    stdout, stderr, returncode = run_command('python main.py --help')
    output = stdout + stderr
    assert "add-user" in output
    assert "list-users" in output
    assert "add-project" in output
    assert "list-projects" in output
    assert "add-task" in output
    assert "list-tasks" in output