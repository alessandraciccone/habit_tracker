from fastapi import APIRouter, Depends, HTTPException
from app.models import Habit, HabitCreate
from app.auth import get_current_user

router = APIRouter()

fake_habits_db = []
habit_id_counter = 1


@router.get("/", response_model=list[Habit])
def get_habits(user: dict = Depends(get_current_user)):
    return [h for h in fake_habits_db if h["owner"] == user["username"]]


@router.post("/", response_model=Habit)
def create_habit(habit: HabitCreate, user: dict = Depends(get_current_user)):
    global habit_id_counter

    new_habit = {
        "id": habit_id_counter,
        "name": habit.name,
        "description": habit.description,
        "owner": user["username"]
    }

    fake_habits_db.append(new_habit)
    habit_id_counter += 1

    return new_habit


@router.delete("/{habit_id}")
def delete_habit(habit_id: int, user: dict = Depends(get_current_user)):
    global fake_habits_db

    for h in fake_habits_db:
        if h["id"] == habit_id and h["owner"] == user["username"]:
            fake_habits_db = [x for x in fake_habits_db if x["id"] != habit_id]
            return {"message": "Habit deleted"}

    raise HTTPException(status_code=404, detail="Habit not found")