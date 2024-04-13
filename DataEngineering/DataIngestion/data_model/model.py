from typing import Union
from pydantic import BaseModel


class SI(BaseModel):
    si_id: str
    si_name: str = None

class Group(BaseModel):
    group_id: str
    group_name: str 
    si_id: str  

class User(BaseModel):
    user_id: str
    user_name: str = None
    group_id: str

class Source(BaseModel):
    source_id: str
    source_name: str = None
    source_info: str = None
    user_id: str
    
class Person(BaseModel):
    person_id: str
    name: str
    full_name: str
    source_id: str
    
class Object(SI, Group, User, Source):
    object_id: str
    track_id: str
    bbox: list[int]
    confidence: float
    image_path: str
    timestamp: int
    fair_face: list[str]
    person_id: list[str]

class Event(BaseModel):
    si_id: str
    group: str
    user_id: str
    source_id: str
    object_id: str
    bbox: list
    conference: float
    image_path: str
    time_stamp: str
    fair_face: list
    person_id: list
    dist: list