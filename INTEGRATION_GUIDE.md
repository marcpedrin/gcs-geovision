# GeoVision Campus Security - Backend Integration Guide

## 📋 Overview

This document explains how the FastAPI backend is integrated with your Flutter and web applications.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flutter App (Mobile)                      │
│                    - Authentication                          │
│                    - Real-time Alerts                        │
│                    - Camera Monitoring                       │
│                    - Entry/Exit Logs                         │
└──────────────────────────────────────┬──────────────────────┘
                                       │ HTTP/JSON
                                       ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Web App - Python)              │
│                   http://127.0.0.1:8000                      │
│                                                              │
│  Core Features:                                             │
│  • Authentication & JWT Tokens                             │
│  • User Management                                         │
│  • Camera Management & Monitoring                          │
│  • Real-time Alerts                                        │
│  • Entry/Exit Logging                                      │
│  • Visitor Management                                      │
│  • Dashboard Statistics                                    │
└──────────────────┬───────────────────────────────────────┬──┘
                   │                                       │
                   ↓                                       ↓
        ┌─────────────────────┐          ┌────────────────────────┐
        │  SQLite Database    │          │  Face Recognition API  │
        │  (Development)      │          │  (Optional)            │
        │  gcs.db             │          │  face_server.py        │
        └─────────────────────┘          └────────────────────────┘
```

## 📁 Backend File Structure

```
web_app/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration settings
├── database.py               # Database connection & setup
├── models.py                 # SQLAlchemy ORM models
├── schemas.py                # Pydantic validation schemas
├── auth.py                   # JWT authentication
├── seed.py                   # Database seeding script
├── routers/                  # API endpoint routers
│   ├── auth.py              # Authentication endpoints
│   ├── users.py             # User profile endpoints
│   ├── cameras.py           # Camera management endpoints
│   ├── alerts.py            # Alert management endpoints
│   ├── entry_logs.py        # Entry/Exit log endpoints
│   ├── visitors.py          # Visitor management endpoints
│   └── dashboard.py         # Dashboard statistics endpoints
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose for multi-container setup
├── run.bat                   # Windows startup script
├── run.sh                    # Linux/Mac startup script
└── BACKEND_README.md         # Backend documentation
```

## 🚀 Quick Start

### Option 1: Local Development (Windows)

```bash
# Navigate to web_app directory
cd gcs-geovision/web_app

# Run the startup script
run.bat
```

This will:
1. Create virtual environment
2. Install dependencies
3. Seed database
4. Start the FastAPI server

### Option 2: Local Development (Linux/Mac)

```bash
cd gcs-geovision/web_app
chmod +x run.sh
./run.sh
```

### Option 3: Docker Compose

```bash
cd gcs-geovision/web_app

# Create .env file for production
echo "SECRET_KEY=your-production-secret-key" > .env

# Start all services
docker-compose up -d

# Stop services
docker-compose down
```

## 🔌 API Endpoints

All endpoints are prefixed with `/api`. Base URL: `http://127.0.0.1:8000/api`

### Authentication
```
POST   /api/auth/register      - Register new user
POST   /api/auth/login         - Login user
POST   /api/auth/logout        - Logout user
```

### Users
```
GET    /api/users/me           - Get current user profile
PUT    /api/users/me           - Update current user profile
GET    /api/users/{user_id}    - Get user by ID
```

### Cameras
```
GET    /api/cameras            - List all cameras
POST   /api/cameras            - Create camera (admin)
GET    /api/cameras/{id}       - Get camera details
GET    /api/cameras/{id}/status - Get camera status
PUT    /api/cameras/{id}       - Update camera (admin)
DELETE /api/cameras/{id}       - Delete camera (admin)
```

### Alerts
```
GET    /api/alerts             - List alerts (paginated)
POST   /api/alerts             - Create alert
GET    /api/alerts/{id}        - Get alert details
PUT    /api/alerts/{id}        - Update alert (admin)
DELETE /api/alerts/{id}        - Delete alert (admin)
```

### Entry Logs
```
GET    /api/entry_logs         - List entry logs (paginated)
POST   /api/entry_logs         - Create entry log
GET    /api/entry_logs/{id}    - Get entry log details
```

### Visitors
```
GET    /api/visitors           - List visitors (paginated)
POST   /api/visitors           - Create visitor
GET    /api/visitors/{id}      - Get visitor details
PUT    /api/visitors/{id}      - Update visitor
DELETE /api/visitors/{id}      - Delete visitor (admin)
```

### Dashboard
```
GET    /api/dashboard/stats    - Get dashboard statistics
```

## 🔐 Authentication Flow

### 1. Register User
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@college.edu",
    "password": "secure_password",
    "name": "John Doe",
    "role": "student",
    "student_id": "STU2024001"
  }'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-here",
    "email": "user@college.edu",
    "name": "John Doe",
    "role": "student",
    "created_at": "2024-05-29T10:00:00"
  }
}
```

### 2. Login User
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@college.edu",
    "password": "secure_password"
  }'
```

### 3. Use Token in Requests
```bash
curl -X GET "http://127.0.0.1:8000/api/users/me" \
  -H "Authorization: Bearer <your_token>"
```

## 🗄️ Database Models

### User
- `id` (UUID primary key)
- `email` (unique)
- `password_hash`
- `name`
- `role` (admin, student, faculty)
- `student_id` (unique, optional)
- `phone`, `dept`, `year`
- `face_enrolled` (boolean)
- `profile_picture` (base64)
- `active` (boolean)
- `created_at`, `updated_at` (timestamps)

### Camera
- `id` (UUID)
- `name`
- `location`
- `active` (boolean)
- `latitude`, `longitude` (coordinates)
- `stream_url` (RTSP/HTTP stream)
- `last_update` (timestamp)

### Alert
- `id` (UUID)
- `camera_id` (foreign key)
- `message`
- `severity` (low, medium, high, critical)
- `details`, `image_url` (optional)
- `resolved` (boolean)
- `timestamp`

### EntryLog
- `id` (auto-increment)
- `user_id` (foreign key)
- `camera_id` (foreign key)
- `gate` (entry point)
- `entry_type` (entry, exit, denied)
- `confidence` (0.0-1.0)
- `timestamp`

### Visitor
- `id` (auto-increment)
- `name`, `phone`, `purpose`
- `host`, `dept`, `id_number`
- `status` (On Campus, Checking In, Exited)
- `gate`
- `latitude`, `longitude`
- `check_in_time`, `check_out_time`

## 🔄 Flutter Integration

### In Flutter ApiService:
```dart
// Base URL is already configured
static const String baseUrl = 'http://127.0.0.1:8000/api';

// Token is automatically included in headers
Map<String, String> _headers() => {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  if (_token != null) 'Authorization': 'Bearer $_token',
};
```

### Example API Calls in Flutter:
```dart
// Login
final response = await apiService.login('user@college.edu', 'password');
apiService.setToken(response['token']);

// Get user profile
final profile = await apiService.getProfile();

// Get cameras
final cameras = await apiService.getCameraList();

// Create alert
await apiService.createAlert(
  cameraId: 'camera-123',
  message: 'Unauthorized access detected',
  severity: 'high',
);

// Get entry logs
final logs = await apiService.getEntryLogs(page: 1, limit: 50);

// Get dashboard stats
final stats = await apiService.getDashboardStats();
```

## 📊 Sample Data

When you first run the backend with `run.bat` or `run.sh`, the `seed.py` script automatically creates:

- **1 Admin User**: admin@geovision.local / admin123
- **5 Student Users**: student1@college.edu through student5@college.edu / student123
- **1 Faculty User**: faculty@college.edu / faculty123
- **5 Cameras**: at different campus locations
- **8 Sample Alerts**: with various severity levels
- **6 Sample Visitors**: with different statuses

## 🛠️ Development Setup

### Install Dependencies
```bash
cd web_app
pip install -r requirements.txt
```

### Run Development Server
```bash
python main.py
```

### Access Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Database Viewer (if using SQLite)
```bash
# Install SQLite browser
# Then open: gcs.db with SQLite browser
```

## 🐛 Troubleshooting

### Issue: Port 8000 already in use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Issue: "ModuleNotFoundError" for fastapi
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database migration errors
```bash
# Delete old database and reseed
rm gcs.db
python seed.py
```

### Issue: CORS errors in Flutter
- Make sure CORS origins include your Flutter app URL in `config.py`
- For emulator: `http://10.0.2.2:8000`

### Issue: Authentication failing
- Ensure token is being sent in Authorization header
- Check token hasn't expired (24 hours default)

## 📦 Environment Variables

Edit `.env` file to configure:

```env
# API
DEBUG=True                           # Set to False in production

# Database
DATABASE_URL=sqlite:///./gcs.db     # Or PostgreSQL URL

# JWT
SECRET_KEY=your-secret-key-here     # Change in production!
ACCESS_TOKEN_EXPIRE_MINUTES=1440    # 24 hours

# Files
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760            # 10MB
```

## 🚀 Production Deployment

### Using Docker Compose
```bash
docker-compose up -d

# Services:
# - API: http://localhost:8000
# - Database: PostgreSQL on localhost:5432
# - PgAdmin: http://localhost:5050
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Environment for Production
```env
DEBUG=False
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql+psycopg2://user:pass@db-host:5432/db_name
```

## 📝 Logging

All API calls are logged to console in debug mode:
```
[API] GET: http://127.0.0.1:8000/api/cameras
[API] GET Response: 200
```

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT Documentation](https://jwt.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📞 Support

For issues, check:
1. `BACKEND_README.md` in web_app folder
2. API documentation at `/docs` endpoint
3. Console logs for detailed error messages

---

**Last Updated**: May 2026  
**Backend Version**: 1.0.0  
**Framework**: FastAPI 0.104+
