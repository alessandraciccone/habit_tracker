from fastapi import APIRouter

router = APIRouter()
@router.get("/")
def get_habits():
    return {"message": "list of habits"}