# lib/models/user.py

# One to many relationship with projects

#Requires
import uuid

class User:
    def __init__(self, name, email, user_id=None):
        self.name = name
        self.email = email
        if not user_id:
            self._id = str(uuid.uuid4())
        else:
            self._id = user_id
            

        
        
    # Serialization
    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "email": self.email 
        }
        
        
    # String representation
    def __str__(self):
        return str(self.to_dict())
       
        
    # Deserialization
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            user_id=data.get("id")
        )