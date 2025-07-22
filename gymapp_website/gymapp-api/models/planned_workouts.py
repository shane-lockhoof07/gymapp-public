from sqlmodel import Session, select, SQLModel, Field, JSON, Column
from typing import List
from models.base import Base
from models.exercises import ExercisesDB
from models.users import UsersDB
from models import exercises as exercises_models
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class PlannedWorkoutsBase(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = None
    exercises: List[UUID] = Field(default_factory=list, sa_column=Column(JSON))
    exercise_performances: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))


class PlannedWorkoutsDB(Base, PlannedWorkoutsBase, table=True):
    __tablename__ = "planned_workouts"
    user_id: UUID = Field(foreign_key="users.item_id", nullable=False)


class PlannedWorkoutsCreate(BaseModel):
    name: Optional[str] = None
    workout_list: List[ExercisesDB] = Field(default_factory=list)
    notes: Optional[str] = None
    user_id: UUID


def create(session: Session, data: PlannedWorkoutsCreate) -> PlannedWorkoutsDB:
    """Create a new workout"""
    exercises = []
    exercise_performances = []

    for exercise_data in data.workout_list:
        item_id = exercise_data.get('item_id')
        exercise_details = exercise_data.get('exerciseDetails', {})
        sets_data = exercise_data.get('sets', [])
        
        if not item_id:
            new_exercise_data = exercises_models.ExercisesCreate(
                name=exercise_data.get('name', exercise_details.get('name', '')),
                description=exercise_details.get('description', ''),
                category=exercise_details.get('category', 'Strength'),
                equipment=exercise_details.get('equipment', 'None'),
                muscles=exercise_details.get('muscles', []),
                sub_muscles=exercise_details.get('sub_muscles', [])
            )
            new_exercise = exercises_models.create(session, new_exercise_data)
            item_id = new_exercise.item_id
        else:
            db_exercise = session.exec(
                select(ExercisesDB).where(ExercisesDB.item_id == UUID(str(item_id)))
            ).first()
            if not db_exercise:
                new_exercise_data = exercises_models.ExercisesCreate(
                    name=exercise_data.get('name', ''),
                    description=exercise_data.get('description', ''),
                    category=exercise_data.get('category', 'Strength'),
                    equipment=exercise_data.get('equipment', 'None'),
                    muscles=exercise_data.get('muscles', []),
                    sub_muscles=exercise_data.get('sub_muscles', [])
                )
                new_exercise = exercises_models.create(session, new_exercise_data)
                item_id = new_exercise.item_id
        
        exercises.append(item_id)
        
        performance_data = {
            'exercise_id': str(item_id),
            'sets': sets_data
        }
        exercise_performances.append(performance_data)

    db_workout = PlannedWorkoutsDB(
        name=data.name,
        notes=data.notes,
        exercises=exercises,
        exercise_performances=exercise_performances,
        user_id=data.user_id
    ) 
    user_exists = session.exec(
        select(UsersDB).where(UsersDB.item_id == data.user_id)
    ).first()
    if not user_exists:
        raise ValueError(f"User with ID {data.user_id} does not exist in the database.")
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    return db_workout