from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from utils.db import get_session
from utils.auth import hash_password
from models import users as users_models


router = APIRouter(tags=["Users"])


@router.get("/usernames")
def get_usernames(session: Session = Depends(get_session)):
    """Get all usernames"""
    print("Fetching all usernames")
    statement = select(users_models.UsersDB.username)
    usernames = session.exec(statement).all()
    return {"usernames": usernames}


@router.post("/create", response_model=users_models.UsersResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: users_models.UsersCreate,
    session: Session = Depends(get_session)
):
    """Create a new user"""
    existing_user = session.exec(
        select(users_models.UsersDB).where(users_models.UsersDB.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    db_user = users_models.create(session, user)
    return db_user


@router.post("/login", response_model=users_models.UsersResponse, status_code=status.HTTP_200_OK)
def login_user(
    user: users_models.UsersLogin,
    session: Session = Depends(get_session)
):
    """Login a user"""
    db_user = session.exec(
        select(users_models.UsersDB).where(users_models.UsersDB.username == user.username)
    ).first()

    print(f"User password: {user.password}")
    print(f"DB User: {db_user.hashed_password if db_user else 'None'}")
    
    if not db_user or not users_models.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    db_user = users_models.authenticate(session, user.username, user.password)
    
    return db_user


@router.put("/users/{user_id}", response_model=users_models.UsersResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: UUID,
    user_update: users_models.UsersUpdate,
    session: Session = Depends(get_session)
):
    """Update user information"""
    try:
        db_user, updated = users_models.update(session, str(user_id), user_update)
        
        if not updated:
            return HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="No changes were made"
            )
        
        return db_user
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.get("/users/{user_id}", response_model=users_models.UsersResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: UUID,
    session: Session = Depends(get_session)
):
    """Get a specific user by ID"""
    statement = select(users_models.UsersDB).where(users_models.UsersDB.item_id == user_id)
    db_user = session.exec(statement).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db_user