from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import os
from anthropic import Anthropic
import json
from dotenv import load_dotenv

from utils.db import get_session
from models.users import UsersDB
from models.workouts import WorkoutsDB

router = APIRouter(prefix="/analysis", tags=["Analysis"])

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

MODEL_CONFIG = {
    "model": os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307"),
    "max_tokens": int(os.getenv("CLAUDE_MAX_TOKENS", "1500")),
    "temperature": float(os.getenv("CLAUDE_TEMPERATURE", "0.7")),
}

anthropic_client = Anthropic(api_key=api_key)

class AnalysisRequest(BaseModel):
    option: Optional[str] = None
    message: Optional[str] = None
    userData: Dict[str, Any]
    workouts: List[Dict[str, Any]]
    conversationHistory: List[Dict[str, str]] = []

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None

def format_workout_data(workouts: List[Dict[str, Any]], limit: int = 100) -> str:
    """Format workout data for Claude context"""
    sorted_workouts = sorted(workouts, key=lambda x: x['date'], reverse=True)[:limit]
    
    workout_summary = []
    for workout in sorted_workouts:
        workout_info = f"Date: {workout['date']}\n"
        workout_info += f"Name: {workout.get('name', 'Unnamed Workout')}\n"
        workout_info += f"Duration: {workout.get('duration', 'N/A')} minutes\n"
        
        if 'detailed_exercises' in workout:
            workout_info += "Exercises:\n"
            for exercise in workout['detailed_exercises']:
                workout_info += f"  - {exercise['name']}: "
                sets_info = []
                for set_data in exercise.get('sets', []):
                    weight = set_data.get('weight', '0')
                    reps = set_data.get('reps', '0')
                    sets_info.append(f"{weight}lbs x {reps} reps")
                workout_info += ", ".join(sets_info) + "\n"
        
        if workout.get('notes'):
            workout_info += f"Notes: {workout['notes']}\n"
        
        workout_summary.append(workout_info)
    
    return "\n---\n".join(workout_summary)

def format_user_data(user_data: Dict[str, Any]) -> str:
    """Format user data for Claude context"""
    return f"""User Profile:
- Name: {user_data.get('first_name', '')} {user_data.get('last_name', '')}
- Age: {user_data.get('age', 'N/A')}
- Height: {user_data.get('height', 'N/A')} inches
- Weight: {user_data.get('weight', 'N/A')} lbs
- Sex: {user_data.get('sex', 'N/A')}
- Experience: {user_data.get('experience', 'N/A')} years
- Goals: {', '.join(user_data.get('goal', []))}"""

def get_initial_prompt(option: str) -> str:
    """Get the initial system prompt based on the selected option"""
    base_prompt = """You are an expert fitness coach and personal trainer assistant. You have deep knowledge of exercise science, nutrition, and workout programming. You provide personalized, actionable advice based on the user's fitness data and goals.

Important guidelines:
- Be encouraging and motivational while remaining realistic
- Provide specific, actionable recommendations
- Use the user's workout history to inform your advice
- Consider the user's experience level and goals
- Keep responses concise but comprehensive
- Use bullet points for clarity when listing multiple items
"""
    
    option_prompts = {
        "analyze_recent": """Focus on analyzing the user's recent workout patterns and provide insights on:
- Training frequency and consistency
- Exercise selection and muscle group balance
- Progressive overload trends
- Recovery patterns
- Specific recommendations for improvement""",
        
        "plan_workout": """Create a specific workout plan for the user's next session based on:
- Their recent training history
- Muscle groups that need attention
- Their current fitness level and goals
- Appropriate exercise selection and volume
- Include sets, reps, and weight recommendations when possible""",
        
        "make_plan": """Design a structured workout program including:
- Weekly training split
- Exercise selection for each day
- Progression scheme
- Volume and intensity guidelines
- Recovery recommendations
- Duration: typically 4-8 weeks"""
    }
    
    return base_prompt + "\n\n" + option_prompts.get(option, "")

@router.post("/chat", response_model=AnalysisResponse)
async def analyze_workouts(
    request: AnalysisRequest,
    session: Session = Depends(get_session)
):
    """Handle AI analysis requests using Claude"""
    try:
        user_context = format_user_data(request.userData)
        workout_context = format_workout_data(request.workouts)
        
        messages = []
        
        for msg in request.conversationHistory:
            role = "user" if msg["role"] == "Human" else "assistant"
            messages.append({
                "role": role,
                "content": msg["content"]
            })
        
        if request.option:
            system_prompt = get_initial_prompt(request.option)
            user_message = f"""{user_context}

Recent Workout History:
{workout_context}

Based on this information, please provide your analysis and recommendations."""
        else:
            system_prompt = get_initial_prompt("analyze_recent")
            user_message = request.message
        
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.7,
            system=system_prompt,
            messages=messages + [{"role": "user", "content": user_message}]
        )
        
        assistant_message = response.content[0].text
        
        return AnalysisResponse(
            success=True,
            message=assistant_message
        )
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return AnalysisResponse(
            success=False,
            message="I apologize, but I encountered an error processing your request.",
            error=str(e)
        )

@router.get("/usage/{user_id}")
async def get_usage_stats(
    user_id: str,
    session: Session = Depends(get_session)
):
    """Get usage statistics for a user"""
    return {
        "daily_messages_used": 0,
        "daily_limit": 5,
        "last_reset": datetime.now().date().isoformat()
    }