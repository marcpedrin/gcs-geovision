from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    STUDENT = "student"
    FACULTY = "faculty"


class EntryType(str, enum.Enum):
    """Entry/Exit types"""
    ENTRY = "entry"
    EXIT = "exit"
    DENIED = "denied"


class AlertSeverity(str, enum.Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VisitorStatus(str, enum.Enum):
    """Visitor status"""
    ON_CAMPUS = "On Campus"
    CHECKING_IN = "Checking In"
    EXITED = "Exited"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT)
    phone = Column(String, nullable=True)
    dept = Column(String, nullable=True)
    year = Column(String, nullable=True)
    student_id = Column(String, nullable=True, unique=True, index=True)
    face_enrolled = Column(Boolean, default=False)
    profile_picture = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    entry_logs = relationship("EntryLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Camera(Base):
    """Camera model"""
    __tablename__ = "cameras"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    stream_url = Column(String, nullable=True)
    last_update = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    alerts = relationship("Alert", back_populates="camera", cascade="all, delete-orphan")
    entry_logs = relationship("EntryLog", back_populates="camera", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Camera {self.name}>"


class Alert(Base):
    """Alert model"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    camera_id = Column(String, ForeignKey("cameras.id"), nullable=False, index=True)
    message = Column(String, nullable=False)
    severity = Column(SQLEnum(AlertSeverity), default=AlertSeverity.MEDIUM)
    details = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    resolved = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    camera = relationship("Camera", back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert {self.id}>"


class EntryLog(Base):
    """Entry/Exit log model"""
    __tablename__ = "entry_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    camera_id = Column(String, ForeignKey("cameras.id"), nullable=False, index=True)
    gate = Column(String, nullable=False)
    entry_type = Column(SQLEnum(EntryType), default=EntryType.ENTRY)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="entry_logs")
    camera = relationship("Camera", back_populates="entry_logs")
    
    def __repr__(self):
        return f"<EntryLog {self.user_id} - {self.entry_type}>"


class Visitor(Base):
    """Visitor model"""
    __tablename__ = "visitors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    host = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    id_number = Column(String, nullable=False, unique=True, index=True)
    status = Column(SQLEnum(VisitorStatus), default=VisitorStatus.CHECKING_IN)
    gate = Column(String, nullable=False)
    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Visitor {self.name}>"


class DashboardStatSnapshot(Base):
    """Dashboard statistics snapshot"""
    __tablename__ = "dashboard_stats"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total_entries = Column(Integer, default=0)
    total_exits = Column(Integer, default=0)
    active_visitors = Column(Integer, default=0)
    security_alerts = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)
    cameras_online = Column(Integer, default=0)
    cameras_offline = Column(Integer, default=0)
    recent_threats = Column(Text, nullable=True)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<DashboardStatSnapshot {self.timestamp}>"
