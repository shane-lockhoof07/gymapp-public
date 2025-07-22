from sqlmodel import Session, select, SQLModel, Field, JSON, Column
from typing import List
from models.base import Base
from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ExercisesBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    category: Optional[str] = None
    equipment: Optional[str] = None
    muscles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    sub_muscles: List[str] = Field(default_factory=list, sa_column=Column(JSON))

class ExercisesDB(Base, ExercisesBase, table=True):
    __tablename__ = "exercises"


class ExercisesCreate(ExercisesBase):
    pass


def create(session: Session, data: ExercisesCreate) -> ExercisesDB:
    """Create a new exercise"""
    db_exercise = ExercisesDB(**data.dict())
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return db_exercise