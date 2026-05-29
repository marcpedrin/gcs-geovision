# ✅ GeoVision Backend Setup Checklist

Complete this checklist to ensure your FastAPI backend is properly set up.

## 📋 Pre-Setup

- [ ] Python 3.10+ is installed
- [ ] You have access to the web_app folder
- [ ] You understand the project architecture
- [ ] You have reviewed the INTEGRATION_GUIDE.md

## 🚀 Installation

- [ ] Navigate to `gcs-geovision/web_app` folder
- [ ] Run `run.bat` (Windows) or `./run.sh` (Linux/Mac)
- [ ] Wait for virtual environment to be created
- [ ] Wait for dependencies to be installed
- [ ] Wait for database to be seeded
- [ ] Server starts on http://127.0.0.1:8000

## 🔍 Verification

- [ ] Server is running without errors
- [ ] No "Connection refused" errors
- [ ] No "ModuleNotFoundError" messages
- [ ] Database file `gcs.db` exists in web_app folder

## 📚 Documentation

- [ ] Read BACKEND_README.md (setup and usage)
- [ ] Read INTEGRATION_GUIDE.md (architecture and integration)
- [ ] Understand the API endpoints
- [ ] Review the database models

## 🧪 API Testing

- [ ] Access http://127.0.0.1:8000/docs (Swagger UI)
- [ ] Run `python test_api.py` to test all endpoints
- [ ] All tests pass successfully
- [ ] Sample data is created (check database)

## 📱 Flutter Integration

- [ ] Flutter ApiService is using `http://127.0.0.1:8000/api`
- [ ] Token management is implemented
- [ ] Authorization header is being sent
- [ ] Error handling is in place

## 🔐 Security

- [ ] .env file has SECRET_KEY set
- [ ] DEBUG is False in production
- [ ] CORS origins are configured
- [ ] JWT tokens are working

## 🗄️ Database

- [ ] Database is initialized (gcs.db exists)
- [ ] Tables are created
- [ ] Sample data is populated
- [ ] Can view data via SQLite browser (optional)

## 🐛 Troubleshooting

- [ ] Checked port 8000 is not in use
- [ ] Verified Python PATH
- [ ] Confirmed requirements.txt is installed
- [ ] Reset database if needed with seed.py

## 📦 Optional Enhancements

- [ ] Docker setup (docker-compose.yml)
- [ ] PostgreSQL database (production)
- [ ] Advanced logging configuration
- [ ] API rate limiting
- [ ] Email notifications

## 🚀 Ready for Development

- [ ] Backend is fully operational
- [ ] All endpoints are responding
- [ ] Flutter can connect to backend
- [ ] Team is ready to proceed

## 📞 Support Resources

If you encounter issues:

1. **Check logs** - Look at console output for errors
2. **Review docs** - See BACKEND_README.md and INTEGRATION_GUIDE.md
3. **Run tests** - Execute `test_api.py` to identify issues
4. **Clear database** - Delete gcs.db and restart to reseed
5. **Restart server** - Kill process and start again

## 🔗 Quick Links

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **Root Endpoint**: http://127.0.0.1:8000/
- **Backend README**: web_app/BACKEND_README.md
- **Integration Guide**: INTEGRATION_GUIDE.md

---

## Sample Credentials

Use these to test the backend:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@geovision.local | admin123 |
| Student 1 | student1@college.edu | student123 |
| Faculty | faculty@college.edu | faculty123 |

---

**Status**: ✅ Ready when all items are checked

**Last Updated**: May 2026
