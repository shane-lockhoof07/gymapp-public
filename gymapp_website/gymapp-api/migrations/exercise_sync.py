import json
import os
from datetime import datetime
from sqlmodel import Session, select
from models import (
    exercises as exercises_models,
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


def import_exercises_from_json(session: Session, filepath: str = None) -> int:
    """Import exercises from JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "exercises.json")
    
    if not os.path.exists(filepath):
        print(f"No exercises file found at {filepath}")
        return 0
    
    try:
        with open(filepath, 'r') as f:
            exercise_data = json.load(f)
        
        imported_count = 0
        for exercise in exercise_data:
            try:
                existing = session.exec(
                    select(exercises_models.ExercisesDB).where(exercises_models.ExercisesDB.name == exercise['name'])
                ).first()
                
                if existing:
                    continue

                exercise_obj = exercises_models.ExercisesDB(**exercise)
                
                if 'item_id' in exercise:
                    exercise_obj.item_id = UUID(exercise['item_id']) if isinstance(exercise['item_id'], str) else exercise['item_id']
                
                if 'item_created' in exercise:
                    exercise_obj.item_created = datetime.fromisoformat(exercise['item_created']) if isinstance(exercise['item_created'], str) else exercise['item_created']
                else:
                    exercise_obj.create()
                
                if 'item_modified' in exercise:
                    exercise_obj.item_modified = datetime.fromisoformat(exercise['item_modified']) if isinstance(exercise['item_modified'], str) else exercise['item_modified']
                
                session.add(exercise_obj)
                imported_count += 1
                
            except Exception as e:
                print(f"Error importing exercise {exercise.get('name', 'unknown')}: {str(e)}")
                continue
        
        session.commit()
        print(f"Imported {imported_count} exercise from JSON")
        return imported_count
        
    except Exception as e:
        print(f"Error reading exercises file: {str(e)}")
        return 0

def export_exercises_to_json(session: Session, filepath: str = None) -> int:
    """Export exercises to JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "exercises.json")
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        exercises = session.exec(select(exercises_models.ExercisesDB)).all()
        
        exercises_data = []
        for exercise in exercises:
            exercise_dict = {
                'item_id': str(exercise.item_id),
                'item_created': exercise.item_created.isoformat(),
                'item_modified': exercise.item_modified.isoformat(),
                'name': exercise.name,
                'description': exercise.description,
                'category': exercise.category,
                'equipment': exercise.equipment,
                'muscles': exercise.muscles,
                'sub_muscles': exercise.sub_muscles,
            }
            exercises_data.append(exercise_dict)
        
        with open(filepath, 'w') as f:
            json.dump(exercises_data, f, indent=2, default=datetime_serializer)
        
        print(f"Exported {len(exercises_data)} exercises to {filepath}")
        return len(exercises_data)
        
    except Exception as e:
        print(f"Error exporting exercises: {str(e)}")
        return 0

