import json
import os
from datetime import datetime
from sqlmodel import Session, select
from models import (
    planned_workouts as planned_workouts_models,
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


def import_planned_workouts_from_json(session: Session, filepath: str = None) -> int:
    """Import workouts from JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "planned_workouts.json")
    
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
                    select(planned_workouts_models.PlannedWorkoutsDB).where(planned_workouts_models.PlannedWorkoutsDB.item_id == workout['item_id'])
                ).first()
                
                if existing:
                    continue

                workout_obj = planned_workouts_models.PlannedWorkoutsDB(**workout)
                
                if 'item_id' in workout:
                    workout_obj.item_id = UUID(workout['item_id']) if isinstance(workout['item_id'], str) else workout['item_id']
                
                if 'item_created' in workout:
                    workout_obj.item_created = datetime.fromisoformat(workout['item_created']) if isinstance(workout['item_created'], str) else workout_data['item_created']
                else:
                    workout_obj.create()
                
                if 'item_modified' in workout:
                    workout_obj.item_modified = datetime.fromisoformat(workout['item_modified']) if isinstance(workout['item_modified'], str) else workout_data['item_modified']
                
                session.add(workout_obj)
                imported_count += 1
                
            except Exception as e:
                print(f"Error importing exercise {workout.get('item_id', 'unknown')}: {str(e)}")
                continue
        
        session.commit()
        print(f"Imported {imported_count} planned workouts from JSON")
        return imported_count
        
    except Exception as e:
        print(f"Error reading planned workouts file: {str(e)}")
        return 0

def export_planned_workouts_to_json(session: Session, filepath: str = None) -> int:
    """Export workouts to JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "planned_workouts.json")
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        workouts = session.exec(select(planned_workouts_models.PlannedWorkoutsDB)).all()
        
        workouts_data = []
        for workout in workouts:
            exercise_dict = {
                'name': str(workout.name),
                'item_id': str(workout.item_id),
                'item_created': workout.item_created.isoformat(),
                'item_modified': workout.item_modified.isoformat(),
                'name': workout.name,
                'description': workout.description,
                'category': workout.category,
                'equipment': workout.equipment,
                'muscles': workout.muscles,
                'sub_muscles': workout.sub_muscles,
            }
            workouts_data.append(exercise_dict)
        
        with open(filepath, 'w') as f:
            json.dump(workouts_data, f, indent=2, default=datetime_serializer)
        
        print(f"Exported {len(workouts_data)} planned workouts to {filepath}")
        return len(workouts_data)
        
    except Exception as e:
        print(f"Error exporting planned workouts: {str(e)}")
        return 0

