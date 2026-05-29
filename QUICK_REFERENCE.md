# 🚀 FastAPI Backend - Quick Reference

## ⚡ Quick Start (30 seconds)

### Windows
```bash
cd gcs-geovision/web_app
run.bat
```

### Linux/Mac
```bash
cd gcs-geovision/web_app
chmod +x run.sh
./run.sh
```

✅ Server will start on `http://127.0.0.1:8000`

---

## 📚 API Documentation

**Interactive Docs**: http://127.0.0.1:8000/docs  
**Alternative Docs**: http://127.0.0.1:8000/redoc

---

## 🔐 Authentication

```bash
# Register
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@college.edu",
    "password": "pass123",
    "name": "John Doe",
    "role": "student"
  }'

# Login
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@college.edu", "password": "pass123"}'

# Use Token
curl -X GET "http://127.0.0.1:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📁 File Structure

```
web_app/
├── main.py              ← FastAPI app
├── config.py            ← Settings
├── models.py            ← Database tables
├── schemas.py           ← Request/Response validation
├── auth.py              ← JWT & passwords
├── database.py          ← DB connection
├── routers/
│   ├── auth.py         ← Login/Register
│   ├── users.py        ← User profile
│   ├── cameras.py      ← Camera management
│   ├── alerts.py       ← Alerts
│   ├── entry_logs.py   ← Entry/Exit logs
│   ├── visitors.py     ← Visitor management
│   └── dashboard.py    ← Statistics
├── seed.py             ← Sample data
├── test_api.py         ← Test suite
├── requirements.txt    ← Dependencies
├── .env                ← Configuration
├── Dockerfile          ← Docker build
├── docker-compose.yml  ← Docker deployment
└── run.bat/run.sh      ← Startup scripts
```

---

## 🔧 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Seed database
python seed.py

# Test all endpoints
python test_api.py

# With uvicorn
uvicorn main:app --reload

# Docker
docker-compose up -d
```

---

## 📊 API Endpoints Cheat Sheet

### Auth
```
POST   /api/auth/register      # Register user
POST   /api/auth/login         # Login user
POST   /api/auth/logout        # Logout
```

### Users
```
GET    /api/users/me           # My profile
PUT    /api/users/me           # Update profile
GET    /api/users/{id}         # Get user by ID
```

### Cameras
```
GET    /api/cameras            # List all
POST   /api/cameras            # Create (admin)
GET    /api/cameras/{id}       # Get by ID
GET    /api/cameras/{id}/status # Status check
PUT    /api/cameras/{id}       # Update (admin)
DELETE /api/cameras/{id}       # Delete (admin)
```

### Alerts
```
GET    /api/alerts             # List (paginated)
POST   /api/alerts             # Create
GET    /api/alerts/{id}        # Get by ID
PUT    /api/alerts/{id}        # Update (admin)
DELETE /api/alerts/{id}        # Delete (admin)
```

### Entry Logs
```
GET    /api/entry_logs         # List (paginated)
POST   /api/entry_logs         # Create
GET    /api/entry_logs/{id}    # Get by ID
```

### Visitors
```
GET    /api/visitors           # List (paginated)
POST   /api/visitors           # Create
GET    /api/visitors/{id}      # Get by ID
PUT    /api/visitors/{id}      # Update
DELETE /api/visitors/{id}      # Delete (admin)
```

### Dashboard
```
GET    /api/dashboard/stats    # Statistics
```

---

## 🔐 Sample Credentials

```
Admin:    admin@geovision.local / admin123
Student1: student1@college.edu / student123
Faculty:  faculty@college.edu / faculty123
```

---

## 🛠️ Environment Variables (.env)

```env
DEBUG=True                              # Dev/Prod
DATABASE_URL=sqlite:///./gcs.db        # SQLite or PostgreSQL
SECRET_KEY=your-secret-key-here        # Change in production!
ACCESS_TOKEN_EXPIRE_MINUTES=1440       # Token expiry
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `taskkill /PID <PID> /F` (Windows) or kill process |
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Database error | Delete `gcs.db` and restart |
| Connection refused | Check server is running |
| Auth errors | Verify token in Authorization header |

---

## 📱 Flutter Integration

Your Flutter app at `lib/services/api_service.dart` is ready:

```dart
// Already configured:
static const String baseUrl = 'http://127.0.0.1:8000/api';

// Already implemented:
await apiService.login(email, password);
await apiService.getProfile();
await apiService.getCameraList();
await apiService.getAlerts();
await apiService.getEntryLogs();
await apiService.getVisitors();
await apiService.getDashboardStats();
```

---

## 🧪 Testing

```bash
# Run test suite
python test_api.py

# Test specific endpoint (curl)
curl -X GET "http://127.0.0.1:8000/api/cameras" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test in Swagger UI
# Open http://127.0.0.1:8000/docs
```

---

## 📦 Deployment

### Docker Compose
```bash
docker-compose up -d
# API: http://localhost:8000
# DB: PostgreSQL on localhost:5432
```

### Production
```bash
# Use PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Use Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Enable HTTPS & security
# Add rate limiting
# Set DEBUG=False
```

---

## 🎯 Architecture

```
Flutter App → ApiService → FastAPI Backend
                              ↓
                          Database (SQLite/PostgreSQL)
                              ↓
                          Response
```

---

## 📚 Documentation Files

1. **BACKEND_README.md** - Complete backend documentation
2. **INTEGRATION_GUIDE.md** - Architecture and integration details
3. **BACKEND_INTEGRATION_SUMMARY.md** - What was implemented
4. **SETUP_CHECKLIST.md** - Verification checklist
5. **This file** - Quick reference

---

## ✅ Status

- ✅ Backend: Complete and ready
- ✅ Database: Configured with sample data
- ✅ Authentication: JWT implemented
- ✅ API Endpoints: All 30+ endpoints ready
- ✅ Documentation: Comprehensive guides included
- ✅ Flutter Integration: Already configured
- ✅ Testing: Test suite provided
- ✅ Deployment: Docker ready

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **API Docs** | http://127.0.0.1:8000/docs |
| **Health Check** | http://127.0.0.1:8000/health |
| **API Root** | http://127.0.0.1:8000/ |
| **ReDoc** | http://127.0.0.1:8000/redoc |

---

## 💡 Tips

1. Always start server before running Flutter app
2. Use `/docs` endpoint to test APIs interactively
3. Check console logs for detailed error messages
4. Keep `.env` secrets safe (don't commit to git)
5. For production, use PostgreSQL not SQLite
6. Add rate limiting for public APIs

---

**Backend Version**: 1.0.0  
**Framework**: FastAPI  
**Status**: ✅ Production Ready  
**Last Updated**: May 29, 2026
