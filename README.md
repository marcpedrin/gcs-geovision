# GeoVision Campus Security Command Centre

A web-based campus security system with facial recognition for student/staff identification, CCTV monitoring, entry logging, and threat management. 

Powered by a local, browser-based IndexedDB database, it features full Role-Based Access Control (RBAC) separating Security Administrators from normal Users (Students/Staff) along with a responsive mobile-first UI for students.

---

## Architecture Map

```
GCS - GeoVision/
│
├── index.html                  # LOGIN / APP ROOT
├── README.md                   # Project documentation
├── CHANGELOG.md                # Version history
│
├── api/
│   └── db.js                   # IndexedDB Database engine for Users, Logs, and Visitors
│
├── css/
│   ├── shell.css               # Base UI styles, variables, admin shell
│   └── shell.js                # Core UI interactions for the admin shell
│
├── user/
│   ├── user-shell.css          # Mobile-first design system for Student Portal
│   ├── profile.html            # Main student dashboard
│   ├── my-entries.html         # Student entry history
│   ├── face_capture_system.html# Facial data enrolment
│   └── signup-details.html     # Visitor details collection
│
└── admin/
    ├── dashboard.html           # Admin site hub
    ├── visitor-management.html  # Visitor log and Check-in routing
    ├── cctv-feed.html           # Live CCTV grid
    ├── entry-history.html       # Global entry history log
    └── security-threats.html    # Manage and resolve campus threats
```

---

## 🚀 How to Run the App

This application relies on browser storage (IndexedDB & SessionStorage). For the database API and cross-page integrations to work seamlessly, **the app must be run securely on a local web server**.

### Step 1: Start a Local Server
Do **not** just double-click the HTML file. Instead, use a local server:

- **Option A (VS Code):** Use the [Live Server Extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer). Right-click `index.html` and select **"Open with Live Server"**.
- **Option B (Node.js):**
  ```bash
  npx serve .
  ```
- **Option C (Python):**
  ```bash
  python -m http.server 8000
  ```

### Step 2: Open the Application
Navigate to the local URL (e.g. `http://127.0.0.1:5500/index.html` or `http://localhost:8000/index.html`).

### Step 3: Login Credentials
The local database gets seeded automatically upon first load. Use the following built-in accounts:

**🛡️ Administrator Login:**
- **Email:** `admin@reva.edu.in`
- **Password:** `Admin`

**🎓 Student (User) Login:**
- **Email:** `student@reva.edu.in`
- **Password:** `Student`

*(Or you can click the quick-login chips on the sign-in screen to auto-fill these credentials)*

---

## User Roles & Flows

### Admin Flow (Command Centre)
The admin view is heavily inspired by high-end security dashboards. It displays aggregate data, live feeds, and handles campus visitors.
1. Gain access to the global **Dashboard** layout and metrics.
2. Monitor **Live CCTV**.
3. View **Global Entry History** (across all students and staff).
4. Identify & Resolve **Security Threats**.
5. Add and track **Visitor Check-ins**, which integrates with the Face Enrolment camera.

### Student Flow (Mobile Portal)
The user side is a **mobile-first progressive web app style** interface centered around their personal profile.
1. Students login and are routed directly to the **Profile** dashboard.
2. They can update profile details, avatar, and check their overall **Face Enrolment status**.
3. If not enrolled, they route to **Face ID Enrolment** to capture multiple facial angles.
4. They can monitor their personal **Gate Entries & Exits**.

---

## Team Collaboration Guide

This section is for team members to understand how to download, edit, and update the project on GitHub.

### 1. Download (Clone) the Repository
To get a local copy of the project on your computer, run:
```bash
git clone <repository-url>
cd GCS-GeoVision
```

### 2. Get the Latest Changes (Pull)
Before start working, always ensure you have the latest updates from your team:
```bash
git pull origin main
```

### 3. Make Changes & Edit
You can now edit the files or any other document. Save your work.

### 4. Upload Your Changes (Commit & Push)
Once you're done editing, follow these steps to upload your changes for the team to see:

**Step A:** Add your changed files:
```bash
git add .
```

**Step B:** Label your changes with a clear message:
```bash
git commit -m "Brief description of what you changed or added"
```

**Step C:** Upload to GitHub:
```bash
git push origin main
```

---

## License

This project is for educational and demonstration purposes.
