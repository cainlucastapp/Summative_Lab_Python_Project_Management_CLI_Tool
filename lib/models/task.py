# lib/models/task.py

# Belongs to one project

# Requires
import uuid


class Task:
    def __init__(self, project_id, title, status="active", task_id=None):
        self.project_id = project_id
        self.title = title
        self.status = status
        if not task_id:
            self._id = str(uuid.uuid4())
        else:
            self._id = task_id
            
        
    # Serialization
    def to_dict(self):
        return {
            "id": self._id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status
        }
        
        
    # String representation
    def __str__(self):
        return str(self.to_dict())
       
        
    # Deserialization
    @classmethod
    def from_dict(cls, data):
        return cls(
            project_id=data.get("project_id"),
            title=data.get("title"),
            status=data.get("status", "active"),
            task_id=data.get("id")
        )