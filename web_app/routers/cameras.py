from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import uuid

from database import get_db
from models import Camera, Alert, AlertSeverity
from schemas import (
    CameraResponse, CameraCreate, CameraUpdate, CameraStatus,
    AlertResponse, AlertCreate, AlertUpdate, AlertListResponse
)
from routers.auth import get_current_user

router = APIRouter(prefix="/cameras", tags=["Cameras"])


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
def get_cameras(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get all cameras"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    cameras = db.query(Camera).all()
    return {
        "cameras": [CameraResponse.model_validate(c) for c in cameras]
    }


@router.post("", response_model=CameraResponse)
def create_camera(
    req: CameraCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create new camera"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    # Check admin
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create cameras"
        )
    
    camera = Camera(
        id=str(uuid.uuid4()),
        name=req.name,
        location=req.location,
        latitude=req.latitude,
        longitude=req.longitude,
        stream_url=req.stream_url,
        active=True
    )
    
    db.add(camera)
    db.commit()
    db.refresh(camera)
    
    return CameraResponse.model_validate(camera)


@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(
    camera_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get camera by ID"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    return CameraResponse.model_validate(camera)


@router.get("/{camera_id}/status", response_model=CameraStatus)
def get_camera_status(
    camera_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get camera status"""
    token = get_token_from_header(authorization)
    get_current_user(token, db)
    
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    return CameraStatus(
        id=camera.id,
        status=camera.active,
        last_update=camera.last_update
    )


@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera(
    camera_id: str,
    req: CameraUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Update camera"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update cameras"
        )
    
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    if req.name is not None:
        camera.name = req.name
    if req.location is not None:
        camera.location = req.location
    if req.active is not None:
        camera.active = req.active
    if req.latitude is not None:
        camera.latitude = req.latitude
    if req.longitude is not None:
        camera.longitude = req.longitude
    if req.stream_url is not None:
        camera.stream_url = req.stream_url
    
    camera.last_update = datetime.utcnow()
    db.commit()
    db.refresh(camera)
    
    return CameraResponse.model_validate(camera)


@router.delete("/{camera_id}")
def delete_camera(
    camera_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Delete camera"""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    
    if user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete cameras"
        )
    
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    db.delete(camera)
    db.commit()
    
    return {"message": "Camera deleted successfully"}
