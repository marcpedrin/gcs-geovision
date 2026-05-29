#!/usr/bin/env python3
"""
Seed script to populate initial database with sample data
Run this after first startup to create sample cameras, users, and alerts
"""

import sys
import os
from datetime import datetime, timedelta
import uuid
import random

# Add web_app to path
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, init_db
from models import User, Camera, Alert, Visitor, VisitorStatus, AlertSeverity, UserRole
from auth import hash_password


def seed_database():
    """Seed database with sample data"""
    
    # Initialize DB
    init_db()
    db = SessionLocal()
    
    print("🌱 Seeding GeoVision Campus Security Database...")
    
    try:
        # Clear existing data
        db.query(User).delete()
        db.query(Camera).delete()
        db.query(Alert).delete()
        db.query(Visitor).delete()
        
        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            email="admin@geovision.local",
            password_hash=hash_password("admin123"),
            name="Admin User",
            role=UserRole.ADMIN,
            phone="+1234567890",
            dept="Administration",
            active=True
        )
        db.add(admin)
        
        # Create sample students
        students = []
        for i in range(5):
            student = User(
                id=str(uuid.uuid4()),
                email=f"student{i+1}@college.edu",
                password_hash=hash_password("student123"),
                name=f"Student User {i+1}",
                role=UserRole.STUDENT,
                student_id=f"STU{2024001+i:05d}",
                phone=f"+123456789{i}",
                dept=["CS", "ECE", "ME", "CE", "EE"][i],
                year="2nd Year",
                face_enrolled=True,
                active=True
            )
            db.add(student)
            students.append(student)
        
        # Create sample faculty
        faculty = User(
            id=str(uuid.uuid4()),
            email="faculty@college.edu",
            password_hash=hash_password("faculty123"),
            name="Faculty Member",
            role=UserRole.FACULTY,
            phone="+1987654321",
            dept="Computer Science",
            active=True
        )
        db.add(faculty)
        
        db.commit()
        print(f"✅ Created {len(students) + 2} users (1 admin, 5 students, 1 faculty)")
        
        # Create cameras
        camera_locations = [
            ("Main Gate", "35.6762°N, 139.6503°E"),
            ("Library Entrance", "35.6763°N, 139.6502°E"),
            ("Parking Lot", "35.6761°N, 139.6504°E"),
            ("Lab Block", "35.6764°N, 139.6501°E"),
            ("Hostel Gate", "35.6760°N, 139.6505°E"),
        ]
        
        cameras = []
        for name, location in camera_locations:
            camera = Camera(
                id=str(uuid.uuid4()),
                name=f"Camera - {name}",
                location=location,
                active=random.choice([True, True, True, False]),
                stream_url=f"rtsp://stream.local/camera_{name.replace(' ', '_').lower()}",
                last_update=datetime.utcnow()
            )
            db.add(camera)
            cameras.append(camera)
        
        db.commit()
        print(f"✅ Created {len(cameras)} cameras")
        
        # Create sample alerts
        alert_messages = [
            "Unauthorized access attempt",
            "Multiple failed authentication",
            "Camera offline",
            "Suspicious activity detected",
            "Motion detected after hours",
            "Unknown person detected",
        ]
        
        for _ in range(8):
            alert = Alert(
                id=str(uuid.uuid4()),
                camera_id=random.choice(cameras).id,
                message=random.choice(alert_messages),
                severity=random.choice([s for s in AlertSeverity]),
                resolved=random.choice([False, False, False, True]),
                timestamp=datetime.utcnow() - timedelta(hours=random.randint(0, 48))
            )
            db.add(alert)
        
        db.commit()
        print("✅ Created 8 sample alerts")
        
        # Create sample visitors
        visitor_purposes = [
            "Official Meeting",
            "Campus Tour",
            "Interview",
            "Delivery",
            "Maintenance",
            "Guest Lecture",
        ]
        
        for i in range(6):
            visitor = Visitor(
                name=f"Visitor {i+1}",
                phone=f"+1234567{900+i:03d}",
                purpose=random.choice(visitor_purposes),
                host=random.choice(students).name,
                dept="Visitor",
                id_number=f"VIS{uuid.uuid4().hex[:8].upper()}",
                status=random.choice([VisitorStatus.ON_CAMPUS, VisitorStatus.EXITED]),
                gate=random.choice(["Main Gate", "Side Gate", "Parking"]),
                check_in_time=datetime.utcnow() - timedelta(hours=random.randint(1, 6))
            )
            if visitor.status == VisitorStatus.EXITED:
                visitor.check_out_time = visitor.check_in_time + timedelta(hours=random.randint(1, 4))
            
            db.add(visitor)
        
        db.commit()
        print("✅ Created 6 sample visitors")
        
        print("\n✨ Database seeded successfully!")
        print("\n📋 Sample Credentials:")
        print("   Admin: admin@geovision.local / admin123")
        print("   Student: student1@college.edu / student123")
        print("   Faculty: faculty@college.edu / faculty123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
