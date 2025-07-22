"""
Migration script to create test users and generate workouts for gym app
"""

import os
import sys
from datetime import datetime, timedelta
from sqlmodel import Session, create_engine
from uuid import uuid4
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import users as users_models
from models import exercises as exercises_models
from models import workouts as workouts_models
from utils.db import get_session, engine
from typing import List, Dict, Any

EXERCISE_POOL = {
    'chest': [
        {'name': 'Barbell Bench Press', 'equipment': 'Barbell', 'muscles': ['Chest'], 'sub_muscles': ['Triceps', 'Shoulders']},
        {'name': 'Incline Dumbbell Press', 'equipment': 'Dumbbells', 'muscles': ['Chest'], 'sub_muscles': ['Shoulders', 'Triceps']},
        {'name': 'Cable Chest Fly', 'equipment': 'Cable Machine', 'muscles': ['Chest'], 'sub_muscles': ['Shoulders']},
        {'name': 'Push-ups', 'equipment': 'None', 'muscles': ['Chest'], 'sub_muscles': ['Triceps', 'Shoulders', 'Core']},
        {'name': 'Dips', 'equipment': 'Dip Bar', 'muscles': ['Chest', 'Triceps'], 'sub_muscles': ['Shoulders']},
    ],
    'back': [
        {'name': 'Pull-ups', 'equipment': 'Pull-up Bar', 'muscles': ['Back', 'Lats'], 'sub_muscles': ['Biceps', 'Core']},
        {'name': 'Bent Over Row', 'equipment': 'Barbell', 'muscles': ['Back'], 'sub_muscles': ['Biceps', 'Rear Delts']},
        {'name': 'Lat Pulldown', 'equipment': 'Cable Machine', 'muscles': ['Lats', 'Back'], 'sub_muscles': ['Biceps']},
        {'name': 'Cable Row', 'equipment': 'Cable Machine', 'muscles': ['Back'], 'sub_muscles': ['Biceps', 'Rear Delts']},
        {'name': 'T-Bar Row', 'equipment': 'Barbell', 'muscles': ['Back'], 'sub_muscles': ['Biceps']},
    ],
    'shoulders': [
        {'name': 'Overhead Press', 'equipment': 'Barbell', 'muscles': ['Shoulders'], 'sub_muscles': ['Triceps', 'Core']},
        {'name': 'Lateral Raises', 'equipment': 'Dumbbells', 'muscles': ['Shoulders'], 'sub_muscles': ['Traps']},
        {'name': 'Front Raises', 'equipment': 'Dumbbells', 'muscles': ['Shoulders'], 'sub_muscles': []},
        {'name': 'Rear Delt Fly', 'equipment': 'Dumbbells', 'muscles': ['Rear Delts'], 'sub_muscles': ['Upper Back']},
        {'name': 'Upright Row', 'equipment': 'Barbell', 'muscles': ['Shoulders', 'Traps'], 'sub_muscles': ['Biceps']},
    ],
    'legs': [
        {'name': 'Barbell Squat', 'equipment': 'Barbell', 'muscles': ['Quads', 'Glutes'], 'sub_muscles': ['Hamstrings', 'Core']},
        {'name': 'Leg Press', 'equipment': 'Machine', 'muscles': ['Quads', 'Glutes'], 'sub_muscles': ['Hamstrings']},
        {'name': 'Romanian Deadlift', 'equipment': 'Barbell', 'muscles': ['Hamstrings', 'Glutes'], 'sub_muscles': ['Back', 'Core']},
        {'name': 'Leg Curls', 'equipment': 'Machine', 'muscles': ['Hamstrings'], 'sub_muscles': ['Calves']},
        {'name': 'Leg Extensions', 'equipment': 'Machine', 'muscles': ['Quads'], 'sub_muscles': []},
        {'name': 'Calf Raises', 'equipment': 'Machine', 'muscles': ['Calves'], 'sub_muscles': []},
    ],
    'arms': [
        {'name': 'Barbell Curl', 'equipment': 'Barbell', 'muscles': ['Biceps'], 'sub_muscles': ['Forearms']},
        {'name': 'Hammer Curl', 'equipment': 'Dumbbells', 'muscles': ['Biceps'], 'sub_muscles': ['Forearms']},
        {'name': 'Tricep Pushdown', 'equipment': 'Cable Machine', 'muscles': ['Triceps'], 'sub_muscles': []},
        {'name': 'Overhead Tricep Extension', 'equipment': 'Dumbbell', 'muscles': ['Triceps'], 'sub_muscles': []},
        {'name': 'Cable Curl', 'equipment': 'Cable Machine', 'muscles': ['Biceps'], 'sub_muscles': ['Forearms']},
    ],
    'core': [
        {'name': 'Plank', 'equipment': 'None', 'muscles': ['Core'], 'sub_muscles': ['Shoulders', 'Glutes']},
        {'name': 'Russian Twists', 'equipment': 'Weight Plate', 'muscles': ['Core', 'Obliques'], 'sub_muscles': []},
        {'name': 'Leg Raises', 'equipment': 'None', 'muscles': ['Core', 'Hip Flexors'], 'sub_muscles': []},
        {'name': 'Cable Crunches', 'equipment': 'Cable Machine', 'muscles': ['Core'], 'sub_muscles': []},
        {'name': 'Ab Wheel', 'equipment': 'Ab Wheel', 'muscles': ['Core'], 'sub_muscles': ['Shoulders', 'Back']},
    ],
    'full_body': [
        {'name': 'Deadlift', 'equipment': 'Barbell', 'muscles': ['Back', 'Glutes', 'Hamstrings'], 'sub_muscles': ['Core', 'Traps']},
        {'name': 'Clean and Press', 'equipment': 'Barbell', 'muscles': ['Shoulders', 'Legs'], 'sub_muscles': ['Core', 'Triceps']},
        {'name': 'Thrusters', 'equipment': 'Barbell', 'muscles': ['Legs', 'Shoulders'], 'sub_muscles': ['Core', 'Triceps']},
        {'name': 'Burpees', 'equipment': 'None', 'muscles': ['Full Body'], 'sub_muscles': ['Core']},
        {'name': 'Battle Ropes', 'equipment': 'Battle Ropes', 'muscles': ['Shoulders', 'Core'], 'sub_muscles': ['Arms', 'Back']},
    ]
}

WORKOUT_TEMPLATES = [
    {'name': 'Push Day', 'muscle_groups': ['chest', 'shoulders', 'arms']},
    {'name': 'Pull Day', 'muscle_groups': ['back', 'arms']},
    {'name': 'Leg Day', 'muscle_groups': ['legs', 'core']},
    {'name': 'Upper Body', 'muscle_groups': ['chest', 'back', 'shoulders', 'arms']},
    {'name': 'Lower Body', 'muscle_groups': ['legs', 'core']},
    {'name': 'Full Body', 'muscle_groups': ['full_body', 'core']},
    {'name': 'Chest & Triceps', 'muscle_groups': ['chest', 'arms']},
    {'name': 'Back & Biceps', 'muscle_groups': ['back', 'arms']},
    {'name': 'Shoulders & Abs', 'muscle_groups': ['shoulders', 'core']},
    {'name': 'HIIT Circuit', 'muscle_groups': ['full_body', 'core']},
]

def create_users(session: Session) -> List[users_models.UsersDB]:
    """Create the three test users"""
    users_data = [
        {
            'username': 'test1',
            'password': 'testuser1',
            'first_name': 'Test',
            'last_name': 'User One',
            'age': 25,
            'height': 70, 
            'weight': 180,
            'sex': 'Male',
            'experience': 2,
            'last_use': datetime.now(),
            'goal': ['strength and lean muscle gain']
        },
        {
            'username': 'test2',
            'password': 'testuser2',
            'first_name': 'Test',
            'last_name': 'User Two',
            'age': 30,
            'height': 72,
            'weight': 200,
            'sex': 'Male',
            'experience': 5,
            'last_use': datetime.now(),
            'goal': ['strength and lean muscle gain']
        },
        {
            'username': 'test3',
            'password': 'testuser3',
            'first_name': 'Test',
            'last_name': 'User Three',
            'age': 28,
            'height': 68,
            'weight': 165,
            'sex': 'Female',
            'experience': 3,
            'last_use': datetime.now(),
            'goal': ['cutting']
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user_create = users_models.UsersCreate(**user_data)
        try:
            user = users_models.create(session, user_create)
            created_users.append(user)
            print(f"Created user: {user.username}")
        except Exception as e:
            print(f"Error creating user {user_data['username']}: {e}")
            from sqlmodel import select
            statement = select(users_models.UsersDB).where(
                users_models.UsersDB.username == user_data['username']
            )
            existing_user = session.exec(statement).first()
            if existing_user:
                created_users.append(existing_user)
                print(f"User {user_data['username']} already exists")
    
    return created_users

def ensure_exercises_exist(session: Session):
    """Create all exercises if they don't exist"""
    from sqlmodel import select
    
    for muscle_group, exercises in EXERCISE_POOL.items():
        for exercise_data in exercises:
            statement = select(exercises_models.ExercisesDB).where(
                exercises_models.ExercisesDB.name == exercise_data['name']
            )
            existing = session.exec(statement).first()
            
            if not existing:
                exercise_create = exercises_models.ExercisesCreate(
                    name=exercise_data['name'],
                    description=f"{exercise_data['name']} exercise",
                    category='Strength',
                    equipment=exercise_data['equipment'],
                    muscles=exercise_data['muscles'],
                    sub_muscles=exercise_data['sub_muscles']
                )
                try:
                    exercises_models.create(session, exercise_create)
                    print(f"Created exercise: {exercise_data['name']}")
                except Exception as e:
                    print(f"Error creating exercise {exercise_data['name']}: {e}")

def get_exercise_by_name(session: Session, name: str) -> exercises_models.ExercisesDB:
    """Get exercise by name"""
    from sqlmodel import select
    statement = select(exercises_models.ExercisesDB).where(
        exercises_models.ExercisesDB.name == name
    )
    return session.exec(statement).first()

def generate_workouts_for_user(session: Session, user: users_models.UsersDB, user_index: int):
    """Generate 50 workouts for a user"""
    
    workout_params = {
        0: {'sets': 3, 'min_reps': 20, 'max_reps': 25, 'weight_range': (20, 70)},
        1: {'sets': 4, 'min_reps': 3, 'max_reps': 6, 'weight_range': (100, 200)},
        2: {'sets': 4, 'min_reps': 12, 'max_reps': 15, 'weight_range': (30, 80)}
    }
    
    params = workout_params[user_index]
    
    for i in range(50):
        template = WORKOUT_TEMPLATES[i % len(WORKOUT_TEMPLATES)]
        workout_date = datetime.now() - timedelta(days=(50 - i))
        
        workout_list = []
        used_exercises = set()
        
        exercise_count = random.randint(4, 6)
        
        for j in range(exercise_count):
            muscle_group = template['muscle_groups'][j % len(template['muscle_groups'])]
            available_exercises = [e for e in EXERCISE_POOL[muscle_group] 
                                 if e['name'] not in used_exercises]
            
            if available_exercises:
                exercise_info = random.choice(available_exercises)
                used_exercises.add(exercise_info['name'])
                
                db_exercise = get_exercise_by_name(session, exercise_info['name'])
                if db_exercise:
                    sets_data = []
                    for set_num in range(params['sets']):
                        weight = random.randint(*params['weight_range'])
                        reps = random.randint(params['min_reps'], params['max_reps'])
                        sets_data.append({
                            'weight': str(weight),
                            'reps': str(reps)
                        })
                    
                    exercise_data = {
                        'item_id': str(db_exercise.item_id),
                        'name': db_exercise.name,
                        'sets': sets_data,
                        'exerciseDetails': {
                            'description': db_exercise.description,
                            'category': db_exercise.category,
                            'equipment': db_exercise.equipment,
                            'muscles': db_exercise.muscles,
                            'sub_muscles': db_exercise.sub_muscles
                        }
                    }
                    workout_list.append(exercise_data)
        
        start_hour = random.randint(6, 20)
        duration_minutes = random.randint(45, 90)
        start_time = workout_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        workout_create = workouts_models.WorkoutsCreate(
            name=f"{template['name']} - Session {i + 1}",
            date=workout_date,
            start_time=start_time,
            end_time=end_time,
            workout_list=workout_list,
            notes=f"Week {i // 7 + 1} - Feeling good!",
            user_id=user.item_id
        )
        
        try:
            workout = workouts_models.create(session, workout_create)
            print(f"Created workout {i + 1} for user {user.username}")
        except Exception as e:
            print(f"Error creating workout: {e}")

def main():
    """Run the migration"""
    print("Starting migration...")
    
    with Session(engine) as session:
        print("\nCreating exercises...")
        ensure_exercises_exist(session)
        
        print("\nCreating users...")
        users = create_users(session)
        
        print("\nGenerating workouts...")
        for i, user in enumerate(users):
            print(f"\nGenerating workouts for {user.username}...")
            generate_workouts_for_user(session, user, i)
    
    print("\nMigration complete!")

if __name__ == "__main__":
    main()