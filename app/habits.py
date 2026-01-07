from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models_sql import HabitDB
from app.models import Habit, HabitCreate
from app.auth import get_current_user

router = APIRouter()
@router.post("/", response_model=Habit)
def get_habits(db:Session=Depends(get_db), user=Depends(get_current_user)):
    habits= db.query(HabitDB).filter(HabitDB.owner_id==user.id).all()
    return habits

@router.post("/", response_model=Habit)
def create_habit(habit:HabitCreate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    new_habit=HabitDB(    
        name=habit.name,
        description=habit.description,
        owner_id=user.id
)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    habit= db.query(HabitDB).filter(HabitDB.id==habit_id, HabitDB.owner_id==user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {"detail":"Habit deleted"}