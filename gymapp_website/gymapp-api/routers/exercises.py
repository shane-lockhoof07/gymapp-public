from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from utils.db import get_session
from utils.auth import hash_password
from models import exercises as exercises_models


router = APIRouter(tags=["Exercises"])


@router.get("/exercises")
def get_exercises(session: Session = Depends(get_session)):
    """Get all exercises"""
    print("Fetching all exercises")
    statement = select(exercises_models.ExercisesDB)
    exercises = session.exec(statement).all()
    statement = select(exercises_models.ExercisesDB.category).distinct()
    categories = session.exec(statement).all()
    statement = select(exercises_models.ExercisesDB.equipment).distinct()
    equipment = session.exec(statement).all() 
    return {"exercises": exercises, "categories": categories, "equipment": equipment}


@router.post("/exercises", response_model=exercises_models.ExercisesDB, status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise: exercises_models.ExercisesCreate,
    session: Session = Depends(get_session)
):
    """Create a new exercise"""
    existing_exercise = session.exec(
        select(exercises_models.ExercisesDB).where(exercises_models.ExercisesDB.name == exercise.name)
    ).first()
    
    if existing_exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise with this name already exists"
        )
    
    db_exercise = exercises_models.create(session, exercise)
    return db_exercise
