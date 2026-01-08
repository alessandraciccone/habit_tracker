from pydantic import BaseModel
from typing import Optional
from datetime import date

class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None


class Habit(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner: str


class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None


class HabitLog(BaseModel):
    habit_id: int
    date: date
    completed: bool