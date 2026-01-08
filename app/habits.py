from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models_sql import HabitDB, HabitLogDB
from app.models import Habit, HabitCreate, HabitLog
from app.auth import get_current_user

router = APIRouter()

# GET tutti gli habits
@router.get("/", response_model=list[Habit])
def get_habits(db: Session = Depends(get_db), user = Depends(get_current_user)):
    habits = db.query(HabitDB).filter(HabitDB.owner_id == user.id).all()
    return [
        {
            "id": h.id,
            "name": h.name,
            "description": h.description,
            "owner": user.username
        }
        for h in habits
    ]

# POST nuovo habit
@router.post("/", response_model=Habit)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    new_habit = HabitDB(    
        name=habit.name,
        description=habit.description,
        owner_id=user.id
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    return {
        "id": new_habit.id,
        "name": new_habit.name,
        "description": new_habit.description,
        "owner": user.username
    }

# DELETE habit
@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id, HabitDB.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {"detail": "Habit deleted"}

# 🆕 POST - Segna un habit come completato per oggi
@router.post("/{habit_id}/log")
def log_habit(habit_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Verifica che l'habit appartenga all'utente
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id, HabitDB.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    today = date.today()
    
    # Controlla se esiste già un log per oggi
    existing_log = db.query(HabitLogDB).filter(
        HabitLogDB.habit_id == habit_id,
        HabitLogDB.date == today
    ).first()
    
    if existing_log:
        # Toggle: se era completato, rimuovi il completamento
        existing_log.completed = 1 if existing_log.completed == 0 else 0
        db.commit()
        db.refresh(existing_log)
        return {
            "habit_id": habit_id,
            "date": str(today),
            "completed": bool(existing_log.completed)
        }
    else:
        # Crea nuovo log
        new_log = HabitLogDB(
            habit_id=habit_id,
            date=today,
            completed=1
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {
            "habit_id": habit_id,
            "date": str(today),
            "completed": True
        }

# 🆕 GET - Ottieni i log di oggi
@router.get("/logs/today")
def get_today_logs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    today = date.today()
    
    # Ottieni tutti gli habits dell'utente
    habits = db.query(HabitDB).filter(HabitDB.owner_id == user.id).all()
    
    result = []
    for habit in habits:
        # Cerca il log di oggi per questo habit
        log = db.query(HabitLogDB).filter(
            HabitLogDB.habit_id == habit.id,
            HabitLogDB.date == today
        ).first()
        
        result.append({
            "habit_id": habit.id,
            "habit_name": habit.name,
            "description": habit.description,
            "completed": bool(log.completed) if log else False,
            "date": str(today)
        })
    
    return result

# 🆕 GET - Ottieni lo storico dei log per un habit
@router.get("/{habit_id}/logs")
def get_habit_logs(habit_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Verifica che l'habit appartenga all'utente
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id, HabitDB.owner_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    logs = db.query(HabitLogDB).filter(HabitLogDB.habit_id == habit_id).order_by(HabitLogDB.date.desc()).all()
    
    return [
        {
            "date": str(log.date),
            "completed": bool(log.completed)
        }
        for log in logs
    ]