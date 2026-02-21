# tests/test_tasks_controller.py

# Requires
import pytest
import tempfile
import os
from lib.controllers.users_controller import UsersController
from lib.controllers.projects_controller import ProjectsController
from lib.controllers.tasks_controller import TasksController
from lib.models.user import User
from lib.models.project import Project
from lib.models.task import Task


# Fixture to create temporary files for testing
@pytest.fixture
def temp_files():
    users_fd, users_path = tempfile.mkstemp(suffix='.json')
    projects_fd, projects_path = tempfile.mkstemp(suffix='.json')
    tasks_fd, tasks_path = tempfile.mkstemp(suffix='.json')
    os.close(users_fd)
    os.close(projects_fd)
    os.close(tasks_fd)
    with open(users_path, 'w') as f:
        f.write('[]')
    with open(projects_path, 'w') as f:
        f.write('[]')
    with open(tasks_path, 'w') as f:
        f.write('[]')
    yield users_path, projects_path, tasks_path
    os.unlink(users_path)
    os.unlink(projects_path)
    os.unlink(tasks_path)


# Task should be added successfully with valid data
def test_add_task_success(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                assert task is not None
                assert task.title == "Create user model"
                assert len(tasks_controller.data) == 1


# Adding task with empty title should fail
def test_add_task_empty_title(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": ""
                }, projects_controller)
                assert task is None
                captured = capsys.readouterr()
                assert "Title cannot be empty" in captured.out


# Adding task with non-existent project should fail
def test_add_task_project_not_found(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": "invalid-id",
                    "title": "Create user model"
                }, projects_controller)
                assert task is None
                captured = capsys.readouterr()
                assert "not found" in captured.out


# Getting task by ID should succeed
def test_get_task_success(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                found = tasks_controller.get_task({"id": task._id}, projects_controller)
                assert found is not None
                assert found._id == task._id


# Getting task with invalid ID should fail
def test_get_task_not_found(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                found = tasks_controller.get_task({"id": "invalid-id"}, projects_controller)
                assert found is None
                captured = capsys.readouterr()
                assert "not found" in captured.out


# Listing tasks with data should succeed
def test_list_tasks_with_data(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create project model"
                }, projects_controller)
                tasks_controller.list_tasks(projects_controller)
                captured = capsys.readouterr()
                assert "Create user model" in captured.out
                assert "Create project model" in captured.out


# Listing tasks with no data should show message
def test_list_tasks_empty(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                tasks_controller.list_tasks(projects_controller)
                captured = capsys.readouterr()
                assert "No tasks found" in captured.out


# Updating task with valid data should succeed
def test_update_task_success(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                updated = tasks_controller.update_task({"id": task._id, "status": "completed"})
                assert updated is not None
                assert updated.status == "completed"


# Updating task with invalid ID should fail
def test_update_task_not_found(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                updated = tasks_controller.update_task({"id": "invalid-id", "status": "completed"})
                assert updated is None
                captured = capsys.readouterr()
                assert "not found" in captured.out


# Updating task with empty title should fail
def test_update_task_empty_title(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                updated = tasks_controller.update_task({"id": task._id, "title": ""})
                assert updated is None
                captured = capsys.readouterr()
                assert "Title cannot be empty" in captured.out


# Updating task with invalid status should fail
def test_update_task_invalid_status(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                updated = tasks_controller.update_task({"id": task._id, "status": "invalid"})
                assert updated is None
                captured = capsys.readouterr()
                assert "active" in captured.out and "completed" in captured.out


# Deleting task should succeed with confirmation
def test_delete_task_success(temp_files, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                deleted = tasks_controller.delete_task({"id": task._id})
                assert deleted is not None
                assert len(tasks_controller.data) == 0


# Deleting task should be cancelled when user says no
def test_delete_task_cancelled(temp_files, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            with TasksController(tasks_file) as tasks_controller:
                task = tasks_controller.add_task({
                    "project_id": project._id,
                    "title": "Create user model"
                }, projects_controller)
                deleted = tasks_controller.delete_task({"id": task._id})
                assert deleted is None
                assert len(tasks_controller.data) == 1
                captured = capsys.readouterr()
                assert "cancelled" in captured.out


# Deleting task with invalid ID should fail
def test_delete_task_not_found(temp_files, capsys):
    users_file, projects_file, tasks_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            with TasksController(tasks_file) as tasks_controller:
                deleted = tasks_controller.delete_task({"id": "invalid-id"})
                assert deleted is None
                captured = capsys.readouterr()
                assert "not found" in captured.out