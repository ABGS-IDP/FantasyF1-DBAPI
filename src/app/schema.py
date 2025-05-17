from pydantic import BaseModel, Field, GetCoreSchemaHandler
from typing import Optional, Any, List
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import EmailStr
from enum import Enum

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
    email: EmailStr
    password: str
    role: Optional[str] = Field(default="player")


class UserStats(BaseModel):
    username: str
    drivers: List[str] = Field(default_factory=list)
    teams: List[str] = Field(default_factory=list)
    total_points: float
    total_budget: float
    bonuses: dict = Field(default_factory=dict)


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
    standings: List[str]


class Score(BaseModel):
    user_id: str
    race_id: str
    points: int


class Bonus(str, Enum):
    twox = "2x"
    beat_teammate = "beat_teammate"
    both_drivers = "both_drivers"