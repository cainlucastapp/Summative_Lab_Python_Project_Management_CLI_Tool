# lib/models/project.py

# One to many relationship with tasks
# Belongs to one user

# Requires
import uuid


class Project:
    def __init__(self, assigned_to_id, title, description, due_date, status="active", project_id=None):
        self.assigned_to_id = assigned_to_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        if not project_id:
            self._id = str(uuid.uuid4())
        else:
            self._id = project_id
            
        
    # Serialization
    def to_dict(self):
        return {
            "id": self._id,
            "assigned_to_id": self.assigned_to_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status
        }
        
        
    # String representation
    def __str__(self):
        return str(self.to_dict())
       
        
    # Deserialization
    @classmethod
    def from_dict(cls, data):
        return cls(
            assigned_to_id=data.get("assigned_to_id"),
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            status=data.get("status", "active"),
            project_id=data.get("id")
        )