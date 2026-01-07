from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserDB(Base):
    __tablename__="users"
    id= Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True)
    full_name=Column(String)
    hashed_password= Column(String)
    habits= relationship("HabitDB", back_populates="owner")

class HabitDB(Base):
    __tablename__="habits"
    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True)
    description= Column(String, nullable=True)
    owner_id= Column(Integer, ForeignKey("users.id"))
    owner= relationship("UserDB", back_populates="habits")
    logs= relationship("HabitLogDB", back_populates="habit")

class HabitLogDB(Base):
    __tablename__="habit_logs"
    id= Column(Integer, primary_key=True, index=True)
    habit_id= Column(Integer, ForeignKey("habits.id"))
    date= Column(Date)
    completed= Column(Integer)  # 0 for False, 1 for True
    habit= relationship("HabitDB", back_populates="logs")