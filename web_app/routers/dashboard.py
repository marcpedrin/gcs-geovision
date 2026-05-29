from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import json

from database import get_db
from models import (
    EntryLog, Alert, Visitor, Camera, VisitorStatus, AlertSeverity,
    DashboardStatSnapshot
)
from schemas import DashboardStatsResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


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


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    # Get stats for today
    today = datetime.utcnow().date()
    
    # Count entries and exits
    total_entries = db.query(func.count(EntryLog.id)).filter(
        EntryLog.entry_type == "entry",
        func.date(EntryLog.timestamp) == today
    ).scalar() or 0
    
    total_exits = db.query(func.count(EntryLog.id)).filter(
        EntryLog.entry_type == "exit",
        func.date(EntryLog.timestamp) == today
    ).scalar() or 0
    
    # Count active visitors
    active_visitors = db.query(func.count(Visitor.id)).filter(
        Visitor.status == VisitorStatus.ON_CAMPUS
    ).scalar() or 0
    
    # Count unresolved alerts
    security_alerts = db.query(func.count(Alert.id)).filter(
        Alert.resolved == False
    ).scalar() or 0
    
    # Average confidence
    avg_confidence = db.query(func.avg(EntryLog.confidence)).scalar() or 0.0
    if avg_confidence:
        avg_confidence = float(avg_confidence)
    
    # Camera status
    cameras_online = db.query(func.count(Camera.id)).filter(
        Camera.active == True
    ).scalar() or 0
    
    cameras_offline = db.query(func.count(Camera.id)).filter(
        Camera.active == False
    ).scalar() or 0
    
    # Recent threats (critical and high severity alerts)
    recent_alerts = db.query(Alert).filter(
        Alert.severity.in_([AlertSeverity.CRITICAL, AlertSeverity.HIGH])
    ).order_by(Alert.timestamp.desc()).limit(5).all()
    
    recent_threats = [alert.message for alert in recent_alerts]
    
    return DashboardStatsResponse(
        total_entries=total_entries,
        total_exits=total_exits,
        active_visitors=active_visitors,
        security_alerts=security_alerts,
        avg_confidence=avg_confidence,
        cameras_online=cameras_online,
        cameras_offline=cameras_offline,
        recent_threats=recent_threats,
        last_updated=datetime.utcnow()
    )
