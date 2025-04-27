from pydantic import BaseModel, Field, GetCoreSchemaHandler
from typing import Optional, List
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler: GetCoreSchemaHandler):
        return core_schema.json_or_python_schema(
            python_schema=core_schema.str_schema(),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

class User(BaseModel):
    username: str
    email: str
    password: str

class Driver(BaseModel):
    name: str
    team: str
    price: float
    championship_points: Optional[int] = Field(default=0)

class DriverUpdateRequest(BaseModel):
    team: Optional[str] = None
    price: Optional[float] = None
    championship_points: Optional[int] = Field(default=0)

class Team(BaseModel):
    name: str
    price: float

class Race(BaseModel):
    name: str
    date: str

class Score(BaseModel):
    user_id: str
    race_id: str
    points: int
