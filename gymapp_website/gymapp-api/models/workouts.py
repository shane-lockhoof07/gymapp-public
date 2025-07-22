from sqlmodel import Session, select, SQLModel, Field, JSON, Column
from typing import List, Dict, Any, Optional
from models.base import Base
from models.exercises import ExercisesDB
from models.users import UsersDB
from models import exercises as exercises_models
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ExercisePerformance(BaseModel):
    """Model for storing exercise performance data"""
    exercise_id: UUID
    sets: List[Dict[str, Any]]


class WorkoutsBase(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    date: datetime = Field(default_factory=datetime.utcnow)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[UUID] = Field(default_factory=list, sa_column=Column(JSON))
    exercise_performances: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))


class WorkoutsDB(Base, WorkoutsBase, table=True):
    __tablename__ = "workouts"
    user_id: UUID = Field(foreign_key="users.item_id", nullable=False)


class WorkoutsCreate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = datetime.utcnow()
    workout_list: List[Dict[str, Any]] = Field(default_factory=list)
    notes: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    user_id: UUID


def create(session: Session, data: WorkoutsCreate) -> WorkoutsDB:
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
    
    if data.start_time and data.end_time:
        data.duration = int((data.end_time - data.start_time).total_seconds() / 60)
    elif data.start_time:
        data.end_time = datetime.now()
        data.duration = int((data.end_time - data.start_time).total_seconds() / 60)
    
    db_workout = WorkoutsDB(
        name=data.name,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        duration=data.duration,
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


def get_workout_with_details(session: Session, workout_id: UUID) -> Dict[str, Any]:
    """Get workout with exercise details and performance data"""
    workout = session.get(WorkoutsDB, workout_id)
    if not workout:
        return None
    
    workout_dict = workout.dict()
    detailed_exercises = []
    
    for i, exercise_id in enumerate(workout.exercises):
        exercise = session.get(ExercisesDB, exercise_id)
        if exercise:
            exercise_data = exercise.dict()
            if i < len(workout.exercise_performances):
                performance = workout.exercise_performances[i]
                exercise_data['sets'] = performance.get('sets', [])
            detailed_exercises.append(exercise_data)
    
    workout_dict['detailed_exercises'] = detailed_exercises
    return workout_dict