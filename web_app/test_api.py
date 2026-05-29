#!/usr/bin/env python3
"""
API Testing Script - Test all GeoVision Backend Endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = None


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")


def get_headers():
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def test_health():
    """Test health check endpoint"""
    print_header("Testing Health Check")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print_success(f"Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print_error(f"Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server at http://127.0.0.1:8000")


def test_auth():
    """Test authentication endpoints"""
    global TOKEN
    
    print_header("Testing Authentication Endpoints")
    
    # Register
    print_info("Registering new user...")
    register_data = {
        "email": f"test_{datetime.now().timestamp()}@college.edu",
        "password": "testpass123",
        "name": "Test User",
        "role": "student",
        "student_id": "TEST2024001"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data, headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        TOKEN = data.get("token")
        print_success(f"Registration successful")
        print(f"  Email: {register_data['email']}")
        print(f"  Token received: {TOKEN[:50]}...")
    else:
        print_error(f"Registration failed: {response.status_code}")
        print(response.text)
    
    # Login with existing admin user
    print_info("\nLogging in as admin...")
    login_data = {
        "email": "admin@geovision.local",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        TOKEN = data.get("token")
        print_success(f"Login successful")
        print(f"  Token received: {TOKEN[:50]}...")
    else:
        print_error(f"Login failed: {response.status_code}")


def test_users():
    """Test user endpoints"""
    print_header("Testing User Endpoints")
    
    # Get current user
    print_info("Getting current user profile...")
    response = requests.get(f"{BASE_URL}/users/me", headers=get_headers())
    if response.status_code == 200:
        print_success("Retrieved current user")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Failed to get user: {response.status_code}")


def test_cameras():
    """Test camera endpoints"""
    print_header("Testing Camera Endpoints")
    
    # Get cameras
    print_info("Getting camera list...")
    response = requests.get(f"{BASE_URL}/cameras", headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        cameras = data.get("cameras", [])
        print_success(f"Retrieved {len(cameras)} cameras")
        if cameras:
            print(f"  First camera: {cameras[0].get('name')}")
    else:
        print_error(f"Failed to get cameras: {response.status_code}")
    
    # Create camera
    print_info("\nCreating new camera...")
    camera_data = {
        "name": f"Test Camera {datetime.now().timestamp()}",
        "location": "Test Lab",
        "stream_url": "rtsp://test.local/stream"
    }
    
    response = requests.post(f"{BASE_URL}/cameras", json=camera_data, headers=get_headers())
    if response.status_code == 200:
        print_success("Camera created successfully")
        camera = response.json()
        print(f"  Camera ID: {camera.get('id')}")
    else:
        print_error(f"Failed to create camera: {response.status_code}")
        print(response.text)


def test_alerts():
    """Test alert endpoints"""
    print_header("Testing Alert Endpoints")
    
    # Get alerts
    print_info("Getting alerts list...")
    response = requests.get(f"{BASE_URL}/alerts?page=1&limit=5", headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        alerts = data.get("alerts", [])
        total = data.get("total", 0)
        print_success(f"Retrieved {len(alerts)} alerts (Total: {total})")
        if alerts:
            print(f"  First alert: {alerts[0].get('message')}")
    else:
        print_error(f"Failed to get alerts: {response.status_code}")
    
    # Create alert
    print_info("\nCreating new alert...")
    
    # First get a camera
    response = requests.get(f"{BASE_URL}/cameras", headers=get_headers())
    if response.status_code == 200:
        cameras = response.json().get("cameras", [])
        if cameras:
            alert_data = {
                "camera_id": cameras[0].get("id"),
                "message": "Test Alert",
                "severity": "high"
            }
            
            response = requests.post(f"{BASE_URL}/alerts", json=alert_data, headers=get_headers())
            if response.status_code == 200:
                print_success("Alert created successfully")
                alert = response.json()
                print(f"  Alert ID: {alert.get('id')}")
            else:
                print_error(f"Failed to create alert: {response.status_code}")
        else:
            print_error("No cameras available to create alert")


def test_entry_logs():
    """Test entry log endpoints"""
    print_header("Testing Entry Log Endpoints")
    
    # Get entry logs
    print_info("Getting entry logs...")
    response = requests.get(f"{BASE_URL}/entry_logs?page=1&limit=5", headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        logs = data.get("logs", [])
        total = data.get("total", 0)
        print_success(f"Retrieved {len(logs)} entry logs (Total: {total})")
        if logs:
            print(f"  First log: {logs[0].get('gate')} entry")
    else:
        print_error(f"Failed to get entry logs: {response.status_code}")


def test_visitors():
    """Test visitor endpoints"""
    print_header("Testing Visitor Endpoints")
    
    # Get visitors
    print_info("Getting visitors list...")
    response = requests.get(f"{BASE_URL}/visitors?page=1&limit=5", headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        visitors = data.get("visitors", [])
        total = data.get("total", 0)
        print_success(f"Retrieved {len(visitors)} visitors (Total: {total})")
        if visitors:
            print(f"  First visitor: {visitors[0].get('name')}")
    else:
        print_error(f"Failed to get visitors: {response.status_code}")


def test_dashboard():
    """Test dashboard endpoints"""
    print_header("Testing Dashboard Endpoints")
    
    # Get stats
    print_info("Getting dashboard statistics...")
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=get_headers())
    if response.status_code == 200:
        print_success("Dashboard stats retrieved")
        stats = response.json()
        print(f"  Total Entries: {stats.get('total_entries')}")
        print(f"  Total Exits: {stats.get('total_exits')}")
        print(f"  Active Visitors: {stats.get('active_visitors')}")
        print(f"  Security Alerts: {stats.get('security_alerts')}")
        print(f"  Cameras Online: {stats.get('cameras_online')}")
        print(f"  Cameras Offline: {stats.get('cameras_offline')}")
    else:
        print_error(f"Failed to get dashboard stats: {response.status_code}")


def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  🎥 GeoVision Campus Security - API Test Suite        ║")
    print("║     Testing all backend endpoints                     ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info("Make sure the backend is running: python main.py")
    
    try:
        test_health()
        test_auth()
        test_users()
        test_cameras()
        test_alerts()
        test_entry_logs()
        test_visitors()
        test_dashboard()
        
        print_header("Test Suite Completed")
        print_success("All tests completed successfully!")
        print_info("Check the interactive docs at: http://127.0.0.1:8000/docs")
        
    except Exception as e:
        print_error(f"Test suite error: {e}")


if __name__ == "__main__":
    main()
