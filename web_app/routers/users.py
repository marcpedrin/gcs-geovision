from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserResponse, UserUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


def get_token_from_header(authorization: str = Header(None)) -> str:
    """Extract token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    return parts[1]


@router.get("/me", response_model=UserResponse)
def get_profile(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
def update_profile(
    req: UserUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    # Update fields
    if req.name is not None:
        user.name = req.name
    if req.phone is not None:
        user.phone = req.phone
    if req.dept is not None:
        user.dept = req.dept
    if req.year is not None:
        user.year = req.year
    if req.profile_picture is not None:
        user.profile_picture = req.profile_picture
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)  # Verify authentication
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)
