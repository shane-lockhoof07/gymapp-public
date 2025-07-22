from sqlmodel import Session, select, SQLModel, Field, JSON, Column
from typing import List
from models.base import Base
from typing import Optional
from datetime import datetime
from utils.auth import hash_password, verify_password
from uuid import UUID
from pydantic import BaseModel


class UsersBase(SQLModel):
    username: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    age: int
    height: int
    weight: int
    sex: str
    experience: int
    last_use: datetime
    goal: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class UsersDB(Base, UsersBase, table=True):
    __tablename__ = "users"
    hashed_password: str


class UsersLogin(BaseModel):
    username: str
    password: str


class UsersCreate(UsersBase):
    password: str


class UsersUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    sex: Optional[str] = None
    experience: Optional[int] = None
    last_use: Optional[datetime] = None
    goal: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    password: Optional[str] = None


class UsersResponse(UsersBase):
    """Response model - excludes password"""
    item_id: UUID
    item_created: datetime
    item_modified: datetime


def create(session: Session, data: UsersCreate) -> UsersDB:
    """Create a new user with hashed password"""
    user_data = data.dict()
    password = user_data.pop('password')
    
    db_user = UsersDB(**user_data, hashed_password=hash_password(password))
    db_user.create()
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update(session: Session, item_id: str, data: UsersUpdate) -> tuple[UsersDB, bool]:
    """Update an existing user"""
    statement = select(UsersDB).where(UsersDB.item_id == item_id)
    db_user = session.exec(statement).first()
    
    if not db_user:
        raise ValueError("User not found")
    
    update_data = data.dict(exclude_unset=True)
    
    if 'password' in update_data:
        password = update_data.pop('password')
        db_user.hashed_password = hash_password(password)
    
    updated = False
    for field, value in update_data.items():
        if value != getattr(db_user, field):
            updated = True
            setattr(db_user, field, value)
    
    if updated or 'password' in data.dict(exclude_unset=True):
        updated = True
        db_user.update()
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    
    return db_user, updated


def authenticate(session: Session, username: str, password: str) -> Optional[UsersDB]:
    """Authenticate a user by username and password"""
    statement = select(UsersDB).where(UsersDB.username == username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    user.last_use = datetime.now()
    user.update()
    session.add(user)
    session.commit()
    
    return user