# tests/test_projects_controller.py

# Requires
import pytest
import tempfile
import os
from lib.controllers.users_controller import UsersController
from lib.controllers.projects_controller import ProjectsController
from lib.models.user import User
from lib.models.project import Project


# Fixture to create temporary files for testing
@pytest.fixture
def temp_files():
    users_fd, users_path = tempfile.mkstemp(suffix='.json')
    projects_fd, projects_path = tempfile.mkstemp(suffix='.json')
    os.close(users_fd)
    os.close(projects_fd)
    with open(users_path, 'w') as f:
        f.write('[]')
    with open(projects_path, 'w') as f:
        f.write('[]')
    yield users_path, projects_path
    os.unlink(users_path)
    os.unlink(projects_path)


# Project should be added successfully with valid data
def test_add_project_success(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            assert project is not None
            assert project.title == "Python CLI Project"
            assert len(projects_controller.data) == 1


# Adding project with empty title should fail
def test_add_project_empty_title(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            assert project is None
            captured = capsys.readouterr()
            assert "Title cannot be empty" in captured.out


# Adding project with empty description should fail
def test_add_project_empty_description(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "",
                "due_date": "12-31-2026"
            }, users_controller)
            assert project is None
            captured = capsys.readouterr()
            assert "Description cannot be empty" in captured.out


# Adding project with invalid date format should fail
def test_add_project_invalid_date_format(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "2026-12-31"
            }, users_controller)
            assert project is None
            captured = capsys.readouterr()
            assert "MM-DD-YYYY format" in captured.out


# Adding project with past due date should fail
def test_add_project_past_date(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "01-01-2020"
            }, users_controller)
            assert project is None
            captured = capsys.readouterr()
            assert "must be in the future" in captured.out


# Adding project with non-existent user should fail
def test_add_project_user_not_found(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": "invalid-id",
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            assert project is None
            captured = capsys.readouterr()
            assert "not found" in captured.out


# Getting project by ID should succeed
def test_get_project_success(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            found = projects_controller.get_project({"id": project._id}, users_controller)
            assert found is not None
            assert found._id == project._id


# Getting project with invalid ID should fail
def test_get_project_not_found(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            found = projects_controller.get_project({"id": "invalid-id"}, users_controller)
            assert found is None
            captured = capsys.readouterr()
            assert "not found" in captured.out


# Listing projects with data should succeed
def test_list_projects_with_data(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "React Dashboard",
                "description": "Build a dashboard application",
                "due_date": "06-30-2027"
            }, users_controller)
            projects_controller.list_projects(users_controller)
            captured = capsys.readouterr()
            assert "Python CLI Project" in captured.out
            assert "React Dashboard" in captured.out


# Listing projects with no data should show message
def test_list_projects_empty(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            projects_controller.list_projects(users_controller)
            captured = capsys.readouterr()
            assert "No projects found" in captured.out


# Updating project with valid data should succeed
def test_update_project_success(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            updated = projects_controller.update_project({"id": project._id, "status": "completed"})
            assert updated is not None
            assert updated.status == "completed"


# Updating project with invalid ID should fail
def test_update_project_not_found(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            updated = projects_controller.update_project({"id": "invalid-id", "status": "completed"})
            assert updated is None
            captured = capsys.readouterr()
            assert "not found" in captured.out


# Updating project with invalid status should fail
def test_update_project_invalid_status(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            updated = projects_controller.update_project({"id": project._id, "status": "invalid"})
            assert updated is None
            captured = capsys.readouterr()
            assert "active" in captured.out and "completed" in captured.out


# Deleting project should succeed with confirmation
def test_delete_project_success(temp_files, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            deleted = projects_controller.delete_project({"id": project._id})
            assert deleted is not None
            assert len(projects_controller.data) == 0


# Deleting project should be cancelled when user says no
def test_delete_project_cancelled(temp_files, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        user = users_controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        with ProjectsController(projects_file) as projects_controller:
            project = projects_controller.add_project({
                "assigned_to_id": user._id,
                "title": "Python CLI Project",
                "description": "Build a project management CLI tool",
                "due_date": "12-31-2026"
            }, users_controller)
            deleted = projects_controller.delete_project({"id": project._id})
            assert deleted is None
            assert len(projects_controller.data) == 1
            captured = capsys.readouterr()
            assert "cancelled" in captured.out


# Deleting project with invalid ID should fail
def test_delete_project_not_found(temp_files, capsys):
    users_file, projects_file = temp_files
    with UsersController(users_file) as users_controller:
        with ProjectsController(projects_file) as projects_controller:
            deleted = projects_controller.delete_project({"id": "invalid-id"})
            assert deleted is None
            captured = capsys.readouterr()
            assert "not found" in captured.out