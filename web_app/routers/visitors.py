from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from database import get_db
from models import Visitor, VisitorStatus
from schemas import (
    VisitorResponse, VisitorCreate, VisitorUpdate, VisitorListResponse
)
from routers.auth import get_current_user

router = APIRouter(prefix="/visitors", tags=["Visitors"])


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
def get_visitors(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    status_filter: str = Query(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get all visitors"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Build query
    query = db.query(Visitor).order_by(desc(Visitor.check_in_time))
    
    # Filter by status if provided
    if status_filter:
        query = query.filter(Visitor.status == status_filter)
    
    total = query.count()
    
    # Pagination
    offset = (page - 1) * limit
    visitors = query.offset(offset).limit(limit).all()
    
    return {
        "visitors": [VisitorResponse.model_validate(v) for v in visitors],
        "total": total,
        "page": page,
        "limit": limit
    }


@router.post("", response_model=dict)
def create_visitor(
    req: VisitorCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create new visitor"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Check if visitor already exists
    existing = db.query(Visitor).filter(
        Visitor.id_number == req.id_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visitor already exists"
        )
    
    visitor = Visitor(
        name=req.name,
        phone=req.phone,
        purpose=req.purpose,
        host=req.host,
        dept=req.dept,
        id_number=req.id_number,
        status=VisitorStatus.CHECKING_IN,
        gate=req.gate,
        latitude=req.latitude,
        longitude=req.longitude
    )
    
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    
    return {
        "visitor": VisitorResponse.model_validate(visitor)
    }


@router.get("/{visitor_id}", response_model=VisitorResponse)
def get_visitor(
    visitor_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get visitor by ID"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found"
        )
    
    return VisitorResponse.model_validate(visitor)


@router.put("/{visitor_id}", response_model=VisitorResponse)
def update_visitor(
    visitor_id: int,
    req: VisitorUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update visitor"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found"
        )
    
    if req.status is not None:
        visitor.status = req.status
    if req.latitude is not None:
        visitor.latitude = req.latitude
    if req.longitude is not None:
        visitor.longitude = req.longitude
    if req.check_out_time is not None:
        visitor.check_out_time = req.check_out_time
    
    db.commit()
    db.refresh(visitor)
    
    return VisitorResponse.model_validate(visitor)


@router.delete("/{visitor_id}")
def delete_visitor(
    visitor_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Delete visitor"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete visitors"
        )
    
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found"
        )
    
    db.delete(visitor)
    db.commit()
    
    return {"message": "Visitor deleted successfully"}
