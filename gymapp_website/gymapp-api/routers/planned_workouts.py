from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List
from datetime import datetime

from utils.db import get_session
from models import planned_workouts as planned_workouts_models
from models import exercises as exercises_models

router = APIRouter(tags=["Planned Workouts"])


@router.get("/planned-workouts")
def get_planned_workouts(user_id: str, session: Session = Depends(get_session)):
    """Get all planned workouts for a user"""
    print(f"Fetching all planned workouts for user {user_id}")
    statement = select(planned_workouts_models.PlannedWorkoutsDB).where(
        planned_workouts_models.PlannedWorkoutsDB.user_id == UUID(user_id)
    )
    planned_workouts = session.exec(statement).all()
    
    for workout in planned_workouts:
        workout.exercise_details = []
        for i, exercise_id in enumerate(workout.exercises):
            exercise = session.get(exercises_models.ExercisesDB, exercise_id)
            if exercise:
                exercise_dict = exercise.dict()
                if i < len(workout.exercise_performances):
                    performance = workout.exercise_performances[i]
                    if performance.get('exercise_id') == str(exercise_id):
                        exercise_dict['sets'] = performance.get('sets', [])
                workout.exercise_details.append(exercise_dict)
    
    return {"planned_workouts": planned_workouts}


@router.post("/planned-workouts", response_model=planned_workouts_models.PlannedWorkoutsDB, status_code=status.HTTP_201_CREATED)
def create_planned_workout(
    workout: planned_workouts_models.PlannedWorkoutsCreate,
    session: Session = Depends(get_session)
):
    """Create a new planned workout"""
    print(f"Creating planned workout for user {workout.user_id}")
    
    try:
        db_workout = planned_workouts_models.create(session, workout)
        return db_workout
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error creating planned workout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create planned workout"
        )


@router.get("/planned-workouts/{workout_id}")
def get_planned_workout(
    workout_id: UUID,
    session: Session = Depends(get_session)
):
    """Get a specific planned workout by ID with exercise details"""
    workout = session.get(planned_workouts_models.PlannedWorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planned workout not found"
        )
    
    workout_dict = {
        "item_id": str(workout.item_id),
        "item_created": workout.item_created,
        "item_modified": workout.item_modified,
        "name": workout.name,
        "notes": workout.notes,
        "user_id": str(workout.user_id),
        "exercises": [str(ex_id) for ex_id in workout.exercises],
        "exercise_performances": workout.exercise_performances,
        "exercise_details": []
    }
    
    for i, exercise_id in enumerate(workout.exercises):
        exercise = session.get(exercises_models.ExercisesDB, exercise_id)
        if exercise:
            exercise_data = {
                "item_id": str(exercise.item_id),
                "name": exercise.name,
                "description": exercise.description,
                "category": exercise.category,
                "equipment": exercise.equipment,
                "muscles": exercise.muscles,
                "sub_muscles": exercise.sub_muscles,
                "sets": []
            }
            
            if i < len(workout.exercise_performances):
                performance = workout.exercise_performances[i]
                if performance.get('exercise_id') == str(exercise_id):
                    exercise_data['sets'] = performance.get('sets', [])
            
            workout_dict['exercise_details'].append(exercise_data)
    
    return workout_dict


@router.put("/planned-workouts/{workout_id}", response_model=planned_workouts_models.PlannedWorkoutsDB)
def update_planned_workout(
    workout_id: UUID,
    workout_update: planned_workouts_models.PlannedWorkoutsBase,
    session: Session = Depends(get_session)
):
    """Update an existing planned workout"""
    workout = session.get(planned_workouts_models.PlannedWorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planned workout not found"
        )
    
    for field, value in workout_update.dict(exclude_unset=True).items():
        setattr(workout, field, value)
    
    workout.item_modified = datetime.utcnow()
    
    session.add(workout)
    session.commit()
    session.refresh(workout)
    
    return workout


@router.delete("/planned-workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_planned_workout(
    workout_id: UUID,
    session: Session = Depends(get_session)
):
    """Delete a planned workout"""
    workout = session.get(planned_workouts_models.PlannedWorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planned workout not found"
        )
    
    session.delete(workout)
    session.commit()
    
    return None