# GeoVision FastAPI Backend

This directory contains a local FastAPI backend for the GeoVision Flutter app.

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/auth/logout`
- `GET /api/users/me`
- `PUT /api/users/me`
- `GET /api/cameras`
- `GET /api/cameras/{camera_id}/status`
- `GET /api/alerts`
- `POST /api/alerts`
- `GET /api/entry_logs`
- `GET /api/visitors`
- `POST /api/visitors`
- `PUT /api/visitors/{id}`
- `DELETE /api/visitors/{id}`

The Flutter app expects the backend at `http://127.0.0.1:8000/api` by default.
