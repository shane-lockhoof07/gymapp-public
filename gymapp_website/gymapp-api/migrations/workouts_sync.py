import json
import os
from datetime import datetime
from sqlmodel import Session, select
from models import (
    workouts as workouts_models,
    exercises as exercises_models,
    users as users_models,
)
from utils.auth import hash_password
from typing import List, Dict, Any
from uuid import UUID

JSON_DATA_PATH = os.getenv("JSON_DATA_PATH", "./reference_data")


def datetime_serializer(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def import_workouts_from_json(session: Session, filepath: str = None) -> int:
    """Import workouts from JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "workouts.json")
    
    if not os.path.exists(filepath):
        print(f"No workouts file found at {filepath}")
        return 0
    
    try:
        with open(filepath, 'r') as f:
            workout_data = json.load(f)
        
        imported_count = 0
        for workout in workout_data:
            try:
                existing = session.exec(
                    select(workouts_models.WorkoutsDB).where(
                        workouts_models.WorkoutsDB.item_id == UUID(workout['item_id'])
                    )
                ).first()
                
                if existing:
                    continue

                workout_obj = workouts_models.WorkoutsDB(
                    item_id=UUID(workout['item_id']) if 'item_id' in workout else None,
                    name=workout.get('name'),
                    date=datetime.fromisoformat(workout['date']) if isinstance(workout['date'], str) else workout['date'],
                    start_time=datetime.fromisoformat(workout['start_time']) if workout.get('start_time') and isinstance(workout['start_time'], str) else workout.get('start_time'),
                    end_time=datetime.fromisoformat(workout['end_time']) if workout.get('end_time') and isinstance(workout['end_time'], str) else workout.get('end_time'),
                    duration=workout.get('duration'),
                    notes=workout.get('notes'),
                    exercises=[UUID(ex_id) for ex_id in workout.get('exercises', [])],
                    exercise_performances=workout.get('exercise_performances', []),
                    user_id=UUID(workout['user_id'])
                )
                
                if 'item_created' in workout:
                    workout_obj.item_created = datetime.fromisoformat(workout['item_created']) if isinstance(workout['item_created'], str) else workout['item_created']
                else:
                    workout_obj.create()
                
                if 'item_modified' in workout:
                    workout_obj.item_modified = datetime.fromisoformat(workout['item_modified']) if isinstance(workout['item_modified'], str) else workout['item_modified']
                
                session.add(workout_obj)
                imported_count += 1
                
            except Exception as e:
                print(f"Error importing workout {workout.get('item_id', 'unknown')}: {str(e)}")
                continue
        
        session.commit()
        print(f"Imported {imported_count} workouts from JSON")
        return imported_count
        
    except Exception as e:
        print(f"Error reading workouts file: {str(e)}")
        return 0


def export_workouts_to_json(session: Session, filepath: str = None) -> int:
    """Export workouts to JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "workouts.json")
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        workouts = session.exec(select(workouts_models.WorkoutsDB)).all()
        
        workouts_data = []
        for workout in workouts:
            workout_dict = {
                'item_id': str(workout.item_id),
                'item_created': workout.item_created.isoformat(),
                'item_modified': workout.item_modified.isoformat(),
                'name': workout.name,
                'date': workout.date.isoformat() if workout.date else None,
                'start_time': workout.start_time.isoformat() if workout.start_time else None,
                'end_time': workout.end_time.isoformat() if workout.end_time else None,
                'duration': workout.duration,
                'notes': workout.notes,
                'exercises': [str(ex_id) for ex_id in workout.exercises],
                'exercise_performances': workout.exercise_performances, 
                'user_id': str(workout.user_id)
            }
            workouts_data.append(workout_dict)
        
        with open(filepath, 'w') as f:
            json.dump(workouts_data, f, indent=2, default=datetime_serializer)
        
        print(f"Exported {len(workouts_data)} workouts to {filepath}")
        return len(workouts_data)
        
    except Exception as e:
        print(f"Error exporting workouts: {str(e)}")
        return 0