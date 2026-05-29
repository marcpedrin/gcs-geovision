from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import EntryLog, User, Camera
from schemas import (
    EntryLogResponse, EntryLogCreate, EntryLogListResponse
)
from routers.auth import get_current_user

router = APIRouter(prefix="/entry_logs", tags=["Entry Logs"])


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


@router.get("", response_model=dict)
def get_entry_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    user_id: str = Query(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get entry logs with pagination"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Build query
    query = db.query(EntryLog).order_by(desc(EntryLog.timestamp))
    
    # Filter by user if provided
    if user_id:
        query = query.filter(EntryLog.user_id == user_id)
    
    total = query.count()
    
    # Pagination
    offset = (page - 1) * limit
    logs = query.offset(offset).limit(limit).all()
    
    return {
        "logs": [EntryLogResponse.model_validate(log) for log in logs],
        "total": total,
        "page": page,
        "limit": limit
    }


@router.post("", response_model=EntryLogResponse)
def create_entry_log(
    req: EntryLogCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create entry log"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Verify user exists
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify camera exists
    camera = db.query(Camera).filter(Camera.id == req.camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    log = EntryLog(
        user_id=req.user_id,
        camera_id=req.camera_id,
        gate=req.gate,
        entry_type=req.entry_type,
        confidence=req.confidence
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    
    return EntryLogResponse.model_validate(log)


@router.get("/{log_id}", response_model=EntryLogResponse)
def get_entry_log(
    log_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get entry log by ID"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    log = db.query(EntryLog).filter(EntryLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry log not found"
        )
    
    return EntryLogResponse.model_validate(log)
