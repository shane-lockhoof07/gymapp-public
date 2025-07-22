import json
import os
from datetime import datetime
from sqlmodel import Session, select
from models import (
    users as users_models,
)
from utils.auth import hash_password
from typing import List, Dict, Any
from uuid import UUID
from .exercise_sync import import_exercises_from_json, export_exercises_to_json
from .workouts_sync import import_workouts_from_json, export_workouts_to_json
from .planned_workouts_sync import import_planned_workouts_from_json, export_planned_workouts_to_json

JSON_DATA_PATH = os.getenv("JSON_DATA_PATH", "./reference_data")

def datetime_serializer(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def import_users_from_json(session: Session, filepath: str = None) -> int:
    """Import users from JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "users.json")
    
    if not os.path.exists(filepath):
        print(f"No users file found at {filepath}")
        return 0
    
    try:
        with open(filepath, 'r') as f:
            users_data = json.load(f)
        
        imported_count = 0
        for user_data in users_data:
            try:
                existing = session.exec(
                    select(users_models.UsersDB).where(users_models.UsersDB.username == user_data['username'])
                ).first()
                
                if existing:
                    print(f"User {user_data['username']} already exists, skipping...")
                    continue
                
                if isinstance(user_data.get('last_use'), str):
                    user_data['last_use'] = datetime.fromisoformat(user_data['last_use'])
                
                if 'hashed_password' in user_data:
                    db_user = users_models.UsersDB(**{k: v for k, v in user_data.items() if k != 'hashed_password'}, 
                                    hashed_password=user_data['hashed_password'])
                elif 'password' in user_data:
                    password = user_data.pop('password')
                    db_user = users_models.UsersDB(**user_data, hashed_password=hash_password(password))
                else:
                    print(f"No password found for user {user_data['username']}, skipping...")
                    continue
                
                if 'item_id' in user_data:
                    db_user.item_id = UUID(user_data['item_id']) if isinstance(user_data['item_id'], str) else user_data['item_id']
                
                if 'item_created' in user_data:
                    db_user.item_created = datetime.fromisoformat(user_data['item_created']) if isinstance(user_data['item_created'], str) else user_data['item_created']
                else:
                    db_user.create()
                
                if 'item_modified' in user_data:
                    db_user.item_modified = datetime.fromisoformat(user_data['item_modified']) if isinstance(user_data['item_modified'], str) else user_data['item_modified']
                
                session.add(db_user)
                imported_count += 1
                
            except Exception as e:
                print(f"Error importing user {user_data.get('username', 'unknown')}: {str(e)}")
                continue
        
        session.commit()
        print(f"Imported {imported_count} users from JSON")
        return imported_count
        
    except Exception as e:
        print(f"Error reading users file: {str(e)}")
        return 0

def export_users_to_json(session: Session, filepath: str = None) -> int:
    """Export users to JSON file"""
    if filepath is None:
        filepath = os.path.join(JSON_DATA_PATH, "users.json")
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        users = session.exec(select(users_models.UsersDB)).all()
        
        users_data = []
        for user in users:
            user_dict = {
                'item_id': str(user.item_id),
                'item_created': user.item_created.isoformat(),
                'item_modified': user.item_modified.isoformat(),
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'height': user.height,
                'weight': user.weight,
                'sex': user.sex,
                'experience': user.experience,
                'last_use': user.last_use.isoformat(),
                'goal': user.goal,
                'hashed_password': user.hashed_password
            }
            users_data.append(user_dict)
        
        with open(filepath, 'w') as f:
            json.dump(users_data, f, indent=2, default=datetime_serializer)
        
        print(f"Exported {len(users_data)} users to {filepath}")
        return len(users_data)
        
    except Exception as e:
        print(f"Error exporting users: {str(e)}")
        return 0

def import_all_data(session: Session):
    """Import all data from JSON files"""
    print("Starting data import...")
    
    import_users_from_json(session)
    import_exercises_from_json(session)
    import_workouts_from_json(session)
    import_planned_workouts_from_json(session)
    
    print("Data import completed")

def export_all_data(session: Session):
    """Export all data to JSON files"""
    print("Starting data export...")
    
    export_users_to_json(session)
    export_exercises_to_json(session)
    export_workouts_to_json(session)
    export_planned_workouts_to_json(session)
    
    print("Data export completed")