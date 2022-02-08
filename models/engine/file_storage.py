#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            return {
                key: value
                for key, value in self.__objects.items()
                if cls in [value.__class__, value.__class__.__name__]
            }

        return self.__objects

    def models(self):
        """return a dictionary of all objects in the database"""
        return classes

    def get(self, cls, id):
        """
          returns an object gotten by its id
            args:
                cls (object): class
                id (string): object id
            returns:
                object: object with the given id 
        """
        if not self.__objects:
            self.reload()

        c_name = cls if isinstance(cls, str) else cls.__name__
        key = c_name + '.' + id
        if key in self.__objects:
            return self.__objects[key]

    def count(self, cls=None):
        """
          returns a count of objects that can be filtered by cls

            args:
                cls (object): class
            returns:
                int: count of objects 
        """
        if not self.__objects:
            self.reload()

        return len(self.all(cls))

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {
            key: self.__objects[key].to_dict() for key in self.__objects}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
