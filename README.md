# Pomodoro Timer App

#### Description

## What it does
- Web-based application which allows the user to keep track of and log Pomodoro sessions. It's a simple productivity tool used to 
enable, practice, and track focused work sessions. 
- Users can run Pomodoro focus sessions and manually start breaks. Completed sessions are automatically logged to a local database. The app provides a history view and basic statistics derived from stored sessions. 

## How to run
Requires Python 3.10+.
```bash
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000

## Features
- Focus/short/long break timer with manual control and completion chime.
- Reliable timing resilient to background tab-throttling
- History page showing completed focus sessions and derived cycle counts
- Account system with register/login and per-user session history 

## Tech used
- Flask for the web app
- SQLite for storage
- Bootstrap 5 for UI styling
- Vanilla JS for timer logic and chimes

## Project structure
- app.py — Flask application and routes
- pomodoro.db — SQLite database (created at runtime)
- templates/ — HTML templates (timer, login, register, history)
- static/ — CSS and client-side JavaScript

## Security note
- Passwords stored as hashed values; session cookies manage logins.
- This project is for educational purposes and does not include production-grade security hardening.

## Design decisions
- The timer uses elapsed wall-clock time instead of setInterval counting to remain accurate when the browser tab is inactive.
- Pomodoro cycles are derived from completed focus sessions rather than stored explicitly, simplifying the data model.
- The app intentionally avoids auto-advancing timers to keep the user in control.

## Future work
- Tags for sessions
- Richer charts/analytics
- PWA support for offline + installability

## Acknowledgements
- Parts of the code and documentation were developed with the assistance of AI tools, with all logic, structure, and final decisions made by the author.
