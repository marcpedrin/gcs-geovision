from __future__ import annotations
import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data.json"

app = FastAPI(title="GeoVision FastAPI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str
    studentId: str
    phone: Optional[str] = None
    dept: Optional[str] = None
    year: Optional[str] = None


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dept: Optional[str] = None
    year: Optional[str] = None
    faceEnrolled: Optional[bool] = None


class AlertRequest(BaseModel):
    camera_id: str
    message: str
    severity: str = Field(default="medium")


class VisitorRequest(BaseModel):
    name: str
    phone: str
    purpose: str
    host: str
    dept: str
    idnum: str
    status: str
    gate: str
    lat: float
    lng: float


def _now() -> str:
    return datetime.utcnow().isoformat()


def _seed_data() -> Dict[str, Any]:
    now = _now()
    return {
        "users": [
            {
                "email": "admin@reva.edu.in",
                "password": "Admin",
                "role": "admin",
                "name": "Admin User",
                "studentId": "ADMIN-001",
                "phone": "+91 90000 00000",
                "dept": "Security",
                "year": "Staff",
                "faceEnrolled": True,
                "pfp": None,
                "joinedAt": now,
            },
            {
                "email": "student@reva.edu.in",
                "password": "Student",
                "role": "student",
                "name": "Demo Student",
                "studentId": "SRN21CV007",
                "phone": "+91 98765 43210",
                "dept": "Computer Science",
                "year": "3rd Year",
                "faceEnrolled": False,
                "pfp": None,
                "joinedAt": now,
            },
        ],
        "cameras": [
            {"id": "cam-01", "name": "Main Gate", "location": "Front Entrance", "status": "online"},
            {"id": "cam-02", "name": "Library", "location": "West Wing", "status": "online"},
            {"id": "cam-03", "name": "Admin Block", "location": "North Corridor", "status": "offline"},
            {"id": "cam-04", "name": "Parking Lot", "location": "South Parking", "status": "online"},
        ],
        "alerts": [
            {"id": 1, "camera_id": "cam-01", "message": "Suspicious movement detected.", "severity": "high", "timestamp": now},
            {"id": 2, "camera_id": "cam-02", "message": "Gate access authorised.", "severity": "low", "timestamp": now},
        ],
        "entry_logs": [
            {
                "id": 1,
                "userId": "student@reva.edu.in",
                "name": "Demo Student",
                "gate": "Main Gate",
                "type": "entry",
                "timestamp": now,
                "confidence": 98.6,
                "dept": "Computer Science",
                "initials": "DS",
                "color": "#059669,#064e3b",
            }
        ],
        "visitors": [
            {
                "id": 1,
                "name": "Ramesh Kumar",
                "phone": "+91 98001 11111",
                "purpose": "Meeting Faculty",
                "host": "Dr. Ravi Shankar",
                "dept": "CS Dept",
                "idnum": "KA-DL-2021-0001234",
                "status": "On Campus",
                "gate": "Main Gate",
                "lat": 12.9121,
                "lng": 77.5221,
                "checkedAt": now,
            }
        ],
    }


def _load_data() -> Dict[str, Any]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data = _seed_data()
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def _save_data(data: Dict[str, Any]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


data = _load_data()
_sessions: Dict[str, str] = {}


def _sanitize_user(user: Dict[str, Any]) -> Dict[str, Any]:
    sanitized = {**user}
    sanitized.pop("password", None)
    return sanitized


def _get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    return next((user for user in data["users"] if user["email"] == email), None)


def _get_user_for_session(token: str) -> Dict[str, Any]:
    email = _sessions.get(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = _get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def _create_token(email: str) -> str:
    token = secrets.token_urlsafe(24)
    _sessions[token] = email
    return token


def _extract_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token missing")
    return authorization.removeprefix("Bearer ")


def _next_id(items: List[Dict[str, Any]]) -> int:
    return max((item.get("id") or 0) for item in items) + 1 if items else 1


def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    token = _extract_token(authorization)
    return _get_user_for_session(token)


@app.get("/api/ping")
def ping():
    return {"status": "ok", "time": _now()}


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    user = _get_user_by_email(payload.email)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = _create_token(user["email"])
    return {"token": token, "user": _sanitize_user(user)}


@app.post("/api/auth/register")
def register(payload: RegisterRequest):
    if _get_user_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = {
        "email": payload.email,
        "password": payload.password,
        "role": "student",
        "name": payload.name,
        "studentId": payload.studentId,
        "phone": payload.phone,
        "dept": payload.dept,
        "year": payload.year,
        "faceEnrolled": False,
        "pfp": None,
        "joinedAt": _now(),
    }
    data["users"].append(user)
    _save_data(data)
    token = _create_token(payload.email)
    return {"token": token, "user": _sanitize_user(user)}


@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    token = _extract_token(authorization)
    _sessions.pop(token, None)
    return {"ok": True}


@app.get("/api/users/me")
def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {"user": _sanitize_user(current_user)}


@app.put("/api/users/me")
def update_profile(payload: ProfileUpdateRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    updated = {**current_user}
    if payload.name is not None:
        updated["name"] = payload.name
    if payload.phone is not None:
        updated["phone"] = payload.phone
    if payload.dept is not None:
        updated["dept"] = payload.dept
    if payload.year is not None:
        updated["year"] = payload.year
    if payload.faceEnrolled is not None:
        updated["faceEnrolled"] = payload.faceEnrolled
    index = next(i for i, user in enumerate(data["users"]) if user["email"] == current_user["email"])
    data["users"][index] = updated
    _save_data(data)
    return {"user": _sanitize_user(updated)}


@app.get("/api/cameras")
def list_cameras():
    return {"cameras": data["cameras"]}


@app.get("/api/cameras/{camera_id}/status")
def camera_status(camera_id: str):
    camera = next((c for c in data["cameras"] if c["id"] == camera_id), None)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    return {
        "camera_id": camera_id,
        "status": camera["status"],
        "name": camera["name"],
        "location": camera["location"],
        "last_seen": _now(),
    }


@app.get("/api/alerts")
def list_alerts(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    alerts = list(reversed(data["alerts"]))
    start = (page - 1) * limit
    end = start + limit
    return {
        "alerts": alerts[start:end],
        "page": page,
        "limit": limit,
        "total": len(alerts),
    }


@app.post("/api/alerts")
def create_alert(payload: AlertRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    alert = {
        "id": _next_id(data["alerts"]),
        "camera_id": payload.camera_id,
        "message": payload.message,
        "severity": payload.severity,
        "timestamp": _now(),
        "created_by": current_user["email"],
    }
    data["alerts"].append(alert)
    _save_data(data)
    return {"ok": True, "alert": alert}


@app.get("/api/entry_logs")
def list_entry_logs(user_id: Optional[str] = Query(None)):
    logs = data["entry_logs"]
    if user_id:
        logs = [log for log in logs if log.get("userId") == user_id or log.get("userId") == user_id]
    logs = list(reversed(logs))
    return {"logs": logs}


@app.get("/api/visitors")
def list_visitors():
    return {"visitors": list(reversed(data["visitors"]))}


@app.post("/api/visitors")
def create_visitor(payload: VisitorRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    visitor = payload.model_dump()
    visitor["id"] = _next_id(data["visitors"])
    visitor["checkedAt"] = _now()
    data["visitors"].append(visitor)
    _save_data(data)
    return {"visitor": visitor}


@app.put("/api/visitors/{visitor_id}")
def update_visitor(visitor_id: int, payload: VisitorRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    visitor = next((v for v in data["visitors"] if v["id"] == visitor_id), None)
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
    updated = {**visitor, **payload.model_dump(), "checkedAt": visitor.get("checkedAt", _now())}
    index = next(i for i, v in enumerate(data["visitors"]) if v["id"] == visitor_id)
    data["visitors"][index] = updated
    _save_data(data)
    return {"visitor": updated}


@app.delete("/api/visitors/{visitor_id}")
def delete_visitor(visitor_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    original = len(data["visitors"])
    data["visitors"] = [v for v in data["visitors"] if v["id"] != visitor_id]
    if len(data["visitors"]) == original:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")
    _save_data(data)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
