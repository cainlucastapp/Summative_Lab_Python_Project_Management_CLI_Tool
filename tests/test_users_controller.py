# tests/test_users_controller.py

# Requires
import pytest
import tempfile
import os
from lib.controllers.users_controller import UsersController
from lib.models.user import User


# Fixture to create a temporary file for testing
@pytest.fixture
def temp_users_file():
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    with open(path, 'w') as f:
        f.write('[]')
    yield path
    os.unlink(path)


# User should be added successfully with valid data
def test_add_user_success(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        assert user is not None
        assert user.name == "George Heeres"
        assert user.email == "george.heeres@flatironschool.com"
        assert len(controller.data) == 1


# Adding user with empty name should fail
def test_add_user_empty_name(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "", "email": "george.heeres@flatironschool.com"})
        assert user is None
        captured = capsys.readouterr()
        assert "Name cannot be empty" in captured.out


# Adding user with name containing numbers should fail
def test_add_user_name_with_numbers(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George123", "email": "george.heeres@flatironschool.com"})
        assert user is None
        captured = capsys.readouterr()
        assert "letters, spaces, periods, hyphens, and apostrophes" in captured.out


# Adding user with invalid name characters should fail
def test_add_user_invalid_name_characters(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George@Heeres", "email": "george.heeres@flatironschool.com"})
        assert user is None
        captured = capsys.readouterr()
        assert "letters, spaces, periods, hyphens, and apostrophes" in captured.out


# Adding user with empty email should fail
def test_add_user_empty_email(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": ""})
        assert user is None
        captured = capsys.readouterr()
        assert "Email cannot be empty" in captured.out


# Adding user with invalid email format should fail
def test_add_user_invalid_email(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "notanemail"})
        assert user is None
        captured = capsys.readouterr()
        assert "Invalid email format" in captured.out


# Adding user with duplicate email should fail
def test_add_user_duplicate_email(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        user = controller.add_user({"name": "Bob Jones", "email": "george.heeres@flatironschool.com"})
        assert user is None
        captured = capsys.readouterr()
        assert "already exists" in captured.out


# Getting user by ID should succeed
def test_get_user_success(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        found = controller.get_user({"id": user._id})
        assert found is not None
        assert found._id == user._id


# Getting user with invalid ID should fail
def test_get_user_not_found(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        found = controller.get_user({"id": "invalid-id"})
        assert found is None
        captured = capsys.readouterr()
        assert "not found" in captured.out


# Listing users with data should succeed
def test_list_users_with_data(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        controller.add_user({"name": "Bob Jones", "email": "bob@example.com"})
        controller.list_users()
        captured = capsys.readouterr()
        assert "George Heeres" in captured.out
        assert "Bob Jones" in captured.out


# Listing users with no data should show message
def test_list_users_empty(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        controller.list_users()
        captured = capsys.readouterr()
        assert "No users found" in captured.out


# Updating user with valid data should succeed
def test_update_user_success(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        updated = controller.update_user({"id": user._id, "name": "George M. Heeres"})
        assert updated is not None
        assert updated.name == "George M. Heeres"


# Updating user with invalid ID should fail
def test_update_user_not_found(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        updated = controller.update_user({"id": "invalid-id", "name": "New Name"})
        assert updated is None
        captured = capsys.readouterr()
        assert "not found" in captured.out


# Updating user with empty name should fail
def test_update_user_empty_name(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        updated = controller.update_user({"id": user._id, "name": ""})
        assert updated is None
        captured = capsys.readouterr()
        assert "Name cannot be empty" in captured.out


# Updating user with duplicate email should fail
def test_update_user_duplicate_email(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        user2 = controller.add_user({"name": "Bob Jones", "email": "bob@example.com"})
        updated = controller.update_user({"id": user2._id, "email": "george.heeres@flatironschool.com"})
        assert updated is None
        captured = capsys.readouterr()
        assert "already in use" in captured.out


# Deleting user should succeed with confirmation
def test_delete_user_success(temp_users_file, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        deleted = controller.delete_user({"id": user._id})
        assert deleted is not None
        assert len(controller.data) == 0


# Deleting user should be cancelled when user says no
def test_delete_user_cancelled(temp_users_file, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    with UsersController(temp_users_file) as controller:
        user = controller.add_user({"name": "George Heeres", "email": "george.heeres@flatironschool.com"})
        deleted = controller.delete_user({"id": user._id})
        assert deleted is None
        assert len(controller.data) == 1
        captured = capsys.readouterr()
        assert "cancelled" in captured.out


# Deleting user with invalid ID should fail
def test_delete_user_not_found(temp_users_file, capsys):
    with UsersController(temp_users_file) as controller:
        deleted = controller.delete_user({"id": "invalid-id"})
        assert deleted is None
        captured = capsys.readouterr()
        assert "not found" in captured.out