from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ════════════════════════════════════════════════════════════════════════════════
# Enums
# ════════════════════════════════════════════════════════════════════════════════

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    FACULTY = "faculty"


class EntryTypeEnum(str, Enum):
    ENTRY = "entry"
    EXIT = "exit"
    DENIED = "denied"


class AlertSeverityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VisitorStatusEnum(str, Enum):
    ON_CAMPUS = "On Campus"
    CHECKING_IN = "Checking In"
    EXITED = "Exited"


# ════════════════════════════════════════════════════════════════════════════════
# Authentication
# ════════════════════════════════════════════════════════════════════════════════

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRoleEnum = UserRoleEnum.STUDENT
    phone: Optional[str] = None
    dept: Optional[str] = None
    year: Optional[str] = None
    student_id: Optional[str] = None


class AuthResponse(BaseModel):
    token: str
    user: "UserResponse"


class TokenData(BaseModel):
    email: Optional[str] = None


# ════════════════════════════════════════════════════════════════════════════════
# User
# ════════════════════════════════════════════════════════════════════════════════

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRoleEnum = UserRoleEnum.STUDENT
    phone: Optional[str] = None
    dept: Optional[str] = None
    year: Optional[str] = None
    student_id: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dept: Optional[str] = None
    year: Optional[str] = None
    profile_picture: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: UserRoleEnum
    phone: Optional[str]
    dept: Optional[str]
    year: Optional[str]
    student_id: Optional[str]
    face_enrolled: bool
    profile_picture: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ════════════════════════════════════════════════════════════════════════════════
# Camera
# ════════════════════════════════════════════════════════════════════════════════

class CameraBase(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    stream_url: Optional[str] = None


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    active: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    stream_url: Optional[str] = None


class CameraStatus(BaseModel):
    id: str
    status: bool
    last_update: Optional[datetime] = None


class CameraResponse(CameraBase):
    id: str
    active: bool
    last_update: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ════════════════════════════════════════════════════════════════════════════════
# Alert
# ════════════════════════════════════════════════════════════════════════════════

class AlertBase(BaseModel):
    camera_id: str
    message: str
    severity: AlertSeverityEnum = AlertSeverityEnum.MEDIUM
    details: Optional[str] = None
    image_url: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    resolved: Optional[bool] = None
    severity: Optional[AlertSeverityEnum] = None


class AlertResponse(AlertBase):
    id: str
    resolved: bool
    timestamp: datetime
    created_at: datetime
    camera: Optional[CameraResponse] = None
    
    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    alerts: List[AlertResponse]
    total: int
    page: int
    limit: int


# ════════════════════════════════════════════════════════════════════════════════
# Entry Log
# ════════════════════════════════════════════════════════════════════════════════

class EntryLogBase(BaseModel):
    user_id: str
    camera_id: str
    gate: str
    entry_type: EntryTypeEnum = EntryTypeEnum.ENTRY
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class EntryLogCreate(EntryLogBase):
    pass


class EntryLogResponse(EntryLogBase):
    id: int
    timestamp: datetime
    user: Optional[UserResponse] = None
    camera: Optional[CameraResponse] = None
    
    class Config:
        from_attributes = True


class EntryLogListResponse(BaseModel):
    logs: List[EntryLogResponse]
    total: int
    page: int
    limit: int


# ════════════════════════════════════════════════════════════════════════════════
# Visitor
# ════════════════════════════════════════════════════════════════════════════════

class VisitorBase(BaseModel):
    name: str
    phone: str
    purpose: str
    host: str
    dept: str
    id_number: str
    gate: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    status: Optional[VisitorStatusEnum] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    check_out_time: Optional[datetime] = None


class VisitorResponse(VisitorBase):
    id: int
    status: VisitorStatusEnum
    check_in_time: datetime
    check_out_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class VisitorListResponse(BaseModel):
    visitors: List[VisitorResponse]
    total: int


# ════════════════════════════════════════════════════════════════════════════════
# Dashboard
# ════════════════════════════════════════════════════════════════════════════════

class DashboardStatsResponse(BaseModel):
    total_entries: int
    total_exits: int
    active_visitors: int
    security_alerts: int
    avg_confidence: float
    cameras_online: int
    cameras_offline: int
    recent_threats: List[str]
    last_updated: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ════════════════════════════════════════════════════════════════════════════════
# Error Response
# ════════════════════════════════════════════════════════════════════════════════

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
