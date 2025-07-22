from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime

from utils.db import get_session
from models import workouts as workouts_models
from models import exercises as exercises_models

router = APIRouter(tags=["Workouts"])


@router.get("/workouts")
def get_workouts(item_id: str, session: Session = Depends(get_session)):
    """Get all workouts for a user"""
    print(f"Fetching all workouts for user {item_id}")
    statement = select(workouts_models.WorkoutsDB).where(
        workouts_models.WorkoutsDB.user_id == UUID(item_id)
    )
    workouts = session.exec(statement).all()
    return {"workouts": workouts}


@router.post("/workouts", response_model=workouts_models.WorkoutsDB, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout: workouts_models.WorkoutsCreate,
    session: Session = Depends(get_session)
):
    """Create a new workout"""
    print(f"Creating workout for user {workout.user_id}")
    
    try:
        db_workout = workouts_models.create(session, workout)
        return db_workout
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error creating workout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create workout"
        )


@router.get("/workouts/{workout_id}")
def get_workout(
    workout_id: UUID,
    session: Session = Depends(get_session)
):
    """Get a specific workout by ID with detailed exercise information"""
    workout = session.get(workouts_models.WorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    workout_dict = {
        "item_id": str(workout.item_id),
        "item_created": workout.item_created,
        "item_modified": workout.item_modified,
        "name": workout.name,
        "date": workout.date,
        "start_time": workout.start_time,
        "end_time": workout.end_time,
        "duration": workout.duration,
        "notes": workout.notes,
        "user_id": str(workout.user_id),
        "exercises": [str(ex_id) for ex_id in workout.exercises],
        "exercise_performances": workout.exercise_performances,
        "detailed_exercises": []
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
            
            workout_dict['detailed_exercises'].append(exercise_data)
    
    return workout_dict


@router.put("/workouts/{workout_id}", response_model=workouts_models.WorkoutsDB)
def update_workout(
    workout_id: UUID,
    workout_update: workouts_models.WorkoutsBase,
    session: Session = Depends(get_session)
):
    """Update an existing workout"""
    workout = session.get(workouts_models.WorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    for field, value in workout_update.dict(exclude_unset=True).items():
        setattr(workout, field, value)
    
    workout.item_modified = datetime.utcnow()
    
    session.add(workout)
    session.commit()
    session.refresh(workout)
    
    return workout


@router.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: UUID,
    session: Session = Depends(get_session)
):
    """Delete a workout"""
    workout = session.get(workouts_models.WorkoutsDB, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    session.delete(workout)
    session.commit()
    
    return None


@router.get("/workouts/{workout_id}/summary")
def get_workout_summary(
    workout_id: UUID,
    session: Session = Depends(get_session)
):
    """Get a workout summary with exercise details for display"""
    workout_data = get_workout(workout_id, session)
    
    total_sets = 0
    total_weight = 0
    total_reps = 0
    
    for exercise in workout_data['detailed_exercises']:
        for set_data in exercise.get('sets', []):
            total_sets += 1
            weight = float(set_data.get('weight', 0) or 0)
            reps = float(set_data.get('reps', 0) or 0)
            total_weight += weight
            total_reps += reps
    
    workout_data['summary'] = {
        'total_exercises': len(workout_data['detailed_exercises']),
        'total_sets': total_sets,
        'total_weight': total_weight,
        'total_reps': total_reps,
        'avg_weight_per_set': total_weight / total_sets if total_sets > 0 else 0,
        'avg_reps_per_set': total_reps / total_sets if total_sets > 0 else 0
    }
    
    return workout_data