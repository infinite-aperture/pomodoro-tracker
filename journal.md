## Project journal

### Session 1
- Set up a clean Python environment (.venv)
- installed flask
- created a minimal flask app (app.py)
- Built a simple pomodoro timer page (/)
- implemented client-side timer logic (25:00, start/pause/reset )
- verified that the app runs on localhost and can be accessed through the browser

### Session 2
- Added a client -> server interaction (POST when timer finishes)
- Created POST endpoint to log completed focus blocks
- triggered a fetch() call when the timer reaches 00:00
- noticed a bug which would stop the timer count-down if safari was minimized
- fixed the bug and made the timer resilient to browser throttling by using elapsed wall-clock time instead of relying on setInterval accuracy

### Session 3
- implemented a "history" page and implemented simple SQLite logic to keep track of completed sessions
- replaced depreciated naive UTC timestamps with timezone-aware UTC datetimes
- started developing a visual language for the app, getting started with a simple logo

### Session 4
- changed visual appereance of the index and history page to make it more appealing
- added improved pomodoro functionality (four 25-Minute blocks with 5 Minute breaks each to complete a whole cycle)
- changed button layout and added required user interaction to progress to the next focus or break block


### Session 5
- Started implementing user-log-in and session cookie -> rebuilt database
- Added Flask secret key to enable secure sessions.
- Added /register route (GET/POST) with Finance-style validation
- stored hashed passwords in users table
- Auto-login after registration via session cookie

### Session 6
- Verified Flask session persistence via session cookie after registration.
- Stabilized authentication stack (register, login, logout, sessions) after resolving missing imports and teardown errors.
- added login_required for protected pages
- added api_login_required for JSON endpoints
- scoped history and session logging to the logged-in user via session["user_id"]

