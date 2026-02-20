# lib/models/person.py

# Requires
import uuid


class Person:
    def __init__(self, name, email):
        self._name = name
        self._email = email
        self._id = str(uuid.uuid4())


    # Name property
    @property
    def name(self):
        return self._name
    

    @name.setter
    def name(self, value):
        self._name = value


    # Email property
    @property
    def email(self):
        return self._email
    
    # Email setter
    @email.setter
    def email(self, value):
        self._email = value


    # ID property (read-only)
    @property
    def id(self):
        return self._id