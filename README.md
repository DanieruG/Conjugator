# Conjugator

A web-based French verb conjugation exercise app with user accounts, customisable exercises, and performance tracking.

## Features

- User registration and login with hashed passwords
- Customisable exercises — choose verbs, tenses, moods, and pronouns
- Timed exercises with per-question answer validation
- Exercise summary with correct/incorrect breakdown
- Historical exercise tracking and statistics dashboard
- Account settings (update email and password)

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy
- **Database:** SQLite (via SQLAlchemy ORM)
- **Conjugation engine:** [verbecc](https://github.com/bretttolbert/verbecc)
- **Templating:** Jinja2
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Custom DSA:** Doubly linked list for question navigation

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DanieruG/Conjugator.git
   cd Conjugator
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000/auth/login
   ```

> The SQLite database (`instance/main_database.db`) is created automatically on first run.

## Project Structure

```
Conjugator/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── instance/
│   └── main_database.db     # SQLite database (auto-generated)
└── app/
    ├── __init__.py          # App factory and database setup
    ├── auth.py              # Login and registration routes
    ├── views.py             # Exercise, dashboard, and settings routes
    ├── models.py            # SQLAlchemy models (Users, Exercises)
    ├── DSA.py               # Doubly linked list for question navigation
    ├── static/
    │   ├── verbs.json       # French verb list with translations
    │   ├── css/             # Stylesheets
    │   └── js/              # Client-side scripts
    └── templates/
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── customiseExercise.html
        ├── exercise.html
        ├── summary.html
        ├── reSummary.html
        ├── settings.html
        └── navBar.html
```

## Scripts

| Script | Description |
|---|---|
| `python main.py` | Starts the Flask development server with debug mode enabled |
