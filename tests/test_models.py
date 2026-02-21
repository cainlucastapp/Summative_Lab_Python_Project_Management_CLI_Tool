# tests/test_models.py

# Requires
import pytest
from lib.models.user import User
from lib.models.project import Project
from lib.models.task import Task


# User should be created with name and email
def test_user_creation():
    user = User(name="Conan The Barbarian", email="conan@cimmeria.com")
    assert user.name == "Conan The Barbarian"
    assert user.email == "conan@cimmeria.com"
    assert user._id is not None


# User should serialize to dictionary
def test_user_to_dict():
    user = User(name="Thulsa Doom", email="thulsa@serpent.com", user_id="test-id-123")
    result = user.to_dict()
    assert result["id"] == "test-id-123"
    assert result["name"] == "Thulsa Doom"
    assert result["email"] == "thulsa@serpent.com"


# User should deserialize from dictionary
def test_user_from_dict():
    data = {"id": "test-id-123", "name": "Conan The Barbarian", "email": "conan@cimmeria.com"}
    user = User.from_dict(data)
    assert user._id == "test-id-123"
    assert user.name == "Conan The Barbarian"
    assert user.email == "conan@cimmeria.com"


# User string representation should return dict string
def test_user_str():
    user = User(name="Thulsa Doom", email="thulsa@serpent.com", user_id="test-id-123")
    result = str(user)
    assert "test-id-123" in result
    assert "Thulsa Doom" in result
    assert "thulsa@serpent.com" in result


# Project should be created with all required fields
def test_project_creation():
    project = Project(
        assigned_to_id="conan-123",
        title="Destroy Tower of Serpents",
        description="Infiltrate and destroy Thulsa Doom's tower",
        due_date="12-31-2026"
    )
    assert project.assigned_to_id == "conan-123"
    assert project.title == "Destroy Tower of Serpents"
    assert project.description == "Infiltrate and destroy Thulsa Doom's tower"
    assert project.due_date == "12-31-2026"
    assert project.status == "active"
    assert project._id is not None


# Project should serialize to dictionary
def test_project_to_dict():
    project = Project(
        assigned_to_id="conan-123",
        title="Rescue King's Daughter",
        description="Save the princess from the cult",
        due_date="12-31-2026",
        status="completed",
        project_id="project-456"
    )
    result = project.to_dict()
    assert result["id"] == "project-456"
    assert result["assigned_to_id"] == "conan-123"
    assert result["title"] == "Rescue King's Daughter"
    assert result["description"] == "Save the princess from the cult"
    assert result["due_date"] == "12-31-2026"
    assert result["status"] == "completed"


# Project should deserialize from dictionary
def test_project_from_dict():
    data = {
        "id": "project-456",
        "assigned_to_id": "thulsa-456",
        "title": "Build Snake Cult Empire",
        "description": "Expand the cult across Hyboria",
        "due_date": "12-31-2026",
        "status": "active"
    }
    project = Project.from_dict(data)
    assert project._id == "project-456"
    assert project.assigned_to_id == "thulsa-456"
    assert project.title == "Build Snake Cult Empire"
    assert project.description == "Expand the cult across Hyboria"
    assert project.due_date == "12-31-2026"
    assert project.status == "active"


# Project string representation should return dict string
def test_project_str():
    project = Project(
        assigned_to_id="conan-123",
        title="Find Atlantean Sword",
        description="Recover the legendary blade",
        due_date="12-31-2026",
        project_id="project-456"
    )
    result = str(project)
    assert "project-456" in result
    assert "Find Atlantean Sword" in result


# Task should be created with all required fields
def test_task_creation():
    task = Task(
        project_id="project-456",
        title="Climb the tower walls"
    )
    assert task.project_id == "project-456"
    assert task.title == "Climb the tower walls"
    assert task.status == "active"
    assert task._id is not None


# Task should serialize to dictionary
def test_task_to_dict():
    task = Task(
        project_id="project-456",
        title="Defeat pit fighters",
        status="completed",
        task_id="task-789"
    )
    result = task.to_dict()
    assert result["id"] == "task-789"
    assert result["project_id"] == "project-456"
    assert result["title"] == "Defeat pit fighters"
    assert result["status"] == "completed"


# Task should deserialize from dictionary
def test_task_from_dict():
    data = {
        "id": "task-789",
        "project_id": "project-456",
        "title": "Break chains of slavery",
        "status": "completed"
    }
    task = Task.from_dict(data)
    assert task._id == "task-789"
    assert task.project_id == "project-456"
    assert task.title == "Break chains of slavery"
    assert task.status == "completed"


# Task string representation should return dict string
def test_task_str():
    task = Task(
        project_id="project-456",
        title="Answer the riddle of steel",
        task_id="task-789"
    )
    result = str(task)
    assert "task-789" in result
    assert "Answer the riddle of steel" in result