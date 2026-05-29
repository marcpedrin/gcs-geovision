# GeoVision Campus Security Backend API

FastAPI-based backend for the GeoVision Campus Security Management System.

## Features

- ✅ User Authentication & Authorization (JWT)
- ✅ User Management (CRUD)
- ✅ Camera Management & Monitoring
- ✅ Security Alerts System
- ✅ Entry/Exit Logs with Face Recognition Confidence
- ✅ Visitor Management System
- ✅ Dashboard Statistics
- ✅ Role-based Access Control (Admin, Student, Faculty)

## Project Structure

```
web_app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection & initialization
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # JWT token & password handling
├── routers/
│   ├── auth.py         # Authentication endpoints
│   ├── users.py        # User profile endpoints
│   ├── cameras.py      # Camera management endpoints
│   ├── alerts.py       # Alert management endpoints
│   ├── entry_logs.py   # Entry/Exit log endpoints
│   ├── visitors.py     # Visitor management endpoints
│   └── dashboard.py    # Dashboard statistics endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.10+
- pip or poetry

### Setup

1. **Install dependencies:**
   ```bash
   cd web_app
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   # Edit .env file with your settings
   # Change SECRET_KEY for production
   ```

3. **Initialize database:**
   ```bash
   # Database will auto-initialize on first run
   ```

## Running the Server

### Development Mode
```bash
cd web_app
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

- **Interactive Docs:** http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs:** http://127.0.0.1:8000/redoc (ReDoc)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{user_id}` - Get user by ID

### Cameras
- `GET /api/cameras` - List all cameras
- `POST /api/cameras` - Create new camera (admin only)
- `GET /api/cameras/{camera_id}` - Get camera details
- `GET /api/cameras/{camera_id}/status` - Get camera status
- `PUT /api/cameras/{camera_id}` - Update camera (admin only)
- `DELETE /api/cameras/{camera_id}` - Delete camera (admin only)

### Alerts
- `GET /api/alerts` - List alerts (paginated)
- `POST /api/alerts` - Create alert
- `GET /api/alerts/{alert_id}` - Get alert details
- `PUT /api/alerts/{alert_id}` - Update alert (admin only)
- `DELETE /api/alerts/{alert_id}` - Delete alert (admin only)

### Entry Logs
- `GET /api/entry_logs` - List entry logs (paginated)
- `POST /api/entry_logs` - Create entry log
- `GET /api/entry_logs/{log_id}` - Get entry log details

### Visitors
- `GET /api/visitors` - List visitors (paginated)
- `POST /api/visitors` - Create visitor
- `GET /api/visitors/{visitor_id}` - Get visitor details
- `PUT /api/visitors/{visitor_id}` - Update visitor
- `DELETE /api/visitors/{visitor_id}` - Delete visitor (admin only)

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. 

**How to authenticate:**

1. **Login** to get token:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
   ```

2. **Use token** in Authorization header:
   ```bash
   curl -X GET "http://127.0.0.1:8000/api/users/me" \
     -H "Authorization: Bearer <your_token>"
   ```

## Database

### SQLite (Default)
- Automatically creates `gcs.db` in the web_app directory
- Good for development and testing

### PostgreSQL (Production)
Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/gcs_db
```

## Environment Variables

```env
# API Configuration
API_TITLE=GeoVision Campus Security API
DEBUG=True

# Database
DATABASE_URL=sqlite:///./gcs.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# File Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
```

## Data Models

### User
- `id` (UUID)
- `email` (unique)
- `password_hash`
- `name`
- `role` (admin, student, faculty)
- `student_id` (optional)
- `phone`, `dept`, `year`
- `face_enrolled` (boolean)
- `profile_picture` (base64)
- `created_at`, `updated_at`

### Camera
- `id` (UUID)
- `name`
- `location`
- `latitude`, `longitude` (optional)
- `stream_url` (optional)
- `active` (boolean)
- `last_update`

### Alert
- `id` (UUID)
- `camera_id` (FK)
- `message`
- `severity` (low, medium, high, critical)
- `details`, `image_url` (optional)
- `resolved` (boolean)
- `timestamp`

### EntryLog
- `id` (auto-increment)
- `user_id` (FK)
- `camera_id` (FK)
- `gate`
- `entry_type` (entry, exit, denied)
- `confidence` (0.0-1.0)
- `timestamp`

### Visitor
- `id` (auto-increment)
- `name`, `phone`, `purpose`
- `host`, `dept`, `id_number`
- `status` (On Campus, Checking In, Exited)
- `gate`
- `latitude`, `longitude` (optional)
- `check_in_time`, `check_out_time`

## Error Handling

All errors return JSON with:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

Common status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## CORS Configuration

Currently allows requests from:
- http://localhost:3000
- http://localhost:5173
- Add more origins in `config.py` as needed

## Testing

```bash
# Test health check
curl http://127.0.0.1:8000/health

# Test API root
curl http://127.0.0.1:8000/

# Open interactive docs
open http://127.0.0.1:8000/docs
```

## Deployment

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t geovision-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... geovision-api
```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## Future Enhancements

- [ ] WebSocket support for real-time alerts
- [ ] Face recognition integration
- [ ] Advanced reporting & analytics
- [ ] Email/SMS notifications
- [ ] Multi-site management
- [ ] API rate limiting
- [ ] Comprehensive logging & audit trails

## Support

For issues or questions, contact the development team.

---

**Last Updated:** May 2026  
**Version:** 1.0.0
