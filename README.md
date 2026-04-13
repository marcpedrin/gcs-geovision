# Campus Security & Facial Recognition System

A web-based campus security system with facial recognition for student/staff identification, CCTV monitoring, entry logging, and threat management.

---

## Architecture Map

```
GCS - GeoVision/
│
├── index.html                  # LOGIN — Main entry point
├── README.md                   # Project documentation
├── CHANGELOG.md                # Version history
│
├── css/
│   └── style.css               # Base wireframe stylesheet (borders & spacing)
│
├── user/
│   ├── signup-details.html     # Enter student/staff details
│   ├── capture-face.html       # Capture facial data
│   └── display-details.html    # Display student details
│
└── admin/
    ├── dashboard.html           # Admin site hub
    ├── cctv-feed.html           # CCTV feed layout
    ├── entry-history.html       # Entry history layout
    └── security-threats.html    # Security threats layout
```

---

## Usage

### Getting Started

1. Open `index.html` in any web browser to reach the **Login** page.
2. From the Login page, navigate to either:
   - **User flow** — Click "Login (User)" or "Sign Up" to begin the user registration process.
   - **Admin flow** — Click "Login (Admin)" to access the admin dashboard.

### User Flow

| Step | Page | Description |
|------|------|-------------|
| 1 | `index.html` | Login or choose to sign up |
| 2 | `user/signup-details.html` | Enter personal and academic details |
| 3 | `user/capture-face.html` | Capture facial data via camera |
| 4 | `user/display-details.html` | Review registered profile and face data |

### Admin Flow

| Step | Page | Description |
|------|------|-------------|
| 1 | `index.html` | Login as administrator |
| 2 | `admin/dashboard.html` | View quick stats and navigate to sub-pages |
| 3 | `admin/cctv-feed.html` | Monitor live CCTV camera feeds |
| 4 | `admin/entry-history.html` | Browse and filter campus entry records |
| 5 | `admin/security-threats.html` | Review and resolve security threats |

### Notes

- All pages are **static HTML wireframes** with no backend logic.
- Buttons and links navigate between pages using relative `href` paths.
- The single `css/style.css` file provides basic borders and spacing for layout structure.
- No JavaScript, frameworks, or external dependencies are used.

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
You can now edit the HTML/CSS files or any other document. Save your work.

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
