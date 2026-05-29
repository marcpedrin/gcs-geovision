from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from database import get_db
from models import Alert, Camera, AlertSeverity
from schemas import (
    AlertResponse, AlertCreate, AlertUpdate, AlertListResponse
)
from routers.auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])


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
def get_alerts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get alerts with pagination"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Query alerts
    query = db.query(Alert).order_by(desc(Alert.timestamp))
    total = query.count()
    
    # Pagination
    offset = (page - 1) * limit
    alerts = query.offset(offset).limit(limit).all()
    
    return {
        "alerts": [AlertResponse.model_validate(a) for a in alerts],
        "total": total,
        "page": page,
        "limit": limit
    }


@router.post("", response_model=AlertResponse)
def create_alert(
    req: AlertCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create new alert"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Verify camera exists
    camera = db.query(Camera).filter(Camera.id == req.camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    alert = Alert(
        id=str(uuid.uuid4()),
        camera_id=req.camera_id,
        message=req.message,
        severity=req.severity,
        details=req.details,
        image_url=req.image_url,
        resolved=False
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return AlertResponse.model_validate(alert)


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get alert by ID"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return AlertResponse.model_validate(alert)


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    req: AlertUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update alert"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update alerts"
        )
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    if req.resolved is not None:
        alert.resolved = req.resolved
    if req.severity is not None:
        alert.severity = req.severity
    
    db.commit()
    db.refresh(alert)
    
    return AlertResponse.model_validate(alert)


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Delete alert"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete alerts"
        )
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alert deleted successfully"}
