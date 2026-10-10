# Running Coach

A running log with automatic personal-record tracking. Log your runs, see your pace by distance, and watch your records update as you add, edit, or delete runs.

Built with Flask and PostgreSQL on the backend and plain HTML, CSS, and JavaScript on the frontend.

## Features

- Register, log in, and log out (JWT stored in HTTP-only cookies, with CSRF protection)
- Log, view, edit, and delete runs (distance, duration, date, perceived effort, notes)
- Pace in seconds per kilometer, calculated for every run
- Personal records for six standard distances, kept in sync automatically:
  1 mile, 2 miles, 5k, 10k, half marathon, marathon
- Dashboard with total distance, run count, average pace per distance category, and your records
- Editable profile (date of birth, sex, experience level, unit preference)

## How personal records work

A run counts toward a standard distance if its distance is within 2% of it (for example, anything from 4,900 m to 5,100 m counts as a 5k). Each user can only have one record per distance.

- **Logging a run** compares it against the current record and replaces the record if it is faster.
- **Editing or deleting a run** recomputes the affected records from all of the user's remaining runs, so a record falls back to the next-best run when needed.

## Tech stack

| Area | Tools |
| --- | --- |
| Backend | Flask 3, Flask-SQLAlchemy, Flask-Migrate (Alembic) |
| Database | PostgreSQL |
| Auth | Flask-JWT-Extended (cookie tokens + CSRF), Flask-Bcrypt |
| Validation | marshmallow |
| Frontend | HTML, vanilla JavaScript, [Pico.css](https://picocss.com) from a CDN |
| Tests | pytest (in-memory SQLite) |

## Getting started

**Requirements:** Python 3.9 or newer, and PostgreSQL running locally.

```bash
# 1. Create the database
createdb running_coach

# 2. Set up the backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# edit .env and set SECRET_KEY, JWT_SECRET_KEY, and DATABASE_URL

# 4. Create the tables
export FLASK_APP=wsgi.py
flask db upgrade

# 5. Run the app
flask run
```

Open <http://127.0.0.1:5000/>. You will be sent to the login page. Register an account to get started.
<img width="1438" height="774" alt="Register page" src="https://github.com/user-attachments/assets/8283c046-fa56-43de-8d56-14c347729617" />
<img width="1440" height="781" alt="Login page" src="https://github.com/user-attachments/assets/7dbd16fb-8e42-4295-8c66-512357d96e8f" />


### Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `JWT_SECRET_KEY` | Signs login tokens | `dev-jwt-secret` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://localhost/running_coach` |


## Running the tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

SQLite does not enforce foreign keys by default, so PostgreSQL is the reference for anything involving constraints.

## API

All endpoints are under `/api/v1`. Everything except register and login requires a valid login cookie, and `POST`, `PATCH`, and `DELETE` requests must send the CSRF token in an `X-CSRF-TOKEN` header (the frontend does this automatically).

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Create an account |
| `POST` | `/auth/login` | Log in and set auth cookies |
| `POST` | `/auth/logout` | Clear auth cookies |
| `GET` | `/auth/me` | Current user |
| `GET` | `/profile/` | Get the profile |
| `PATCH` | `/profile/` | Update the profile |
| `POST` | `/runs` | Log a run |
| `GET` | `/runs` | List your runs |
| `GET` | `/runs/<id>` | Get one run |
| `PATCH` | `/runs/<id>` | Edit a run |
| `DELETE` | `/runs/<id>` | Delete a run |
| `GET` | `/records` | Your personal records |
| `GET` | `/dashboard` | Totals, pace by category, and records |
<img width="1436" height="762" alt="Dashboard" src="https://github.com/user-attachments/assets/89dbc0f8-9b97-4edd-8e8d-1225d17b8b44" />
<img width="1423" height="773" alt="Profile" src="https://github.com/user-attachments/assets/13336c1e-fb49-439d-bbae-fddf212b9e36" />
Example run:

```json
{
  "distance_meters": 5000,
  "duration_seconds": 1500,
  "date": "2026-07-01",
  "perceived_effort": "moderate",
  "notes": "Felt strong"
}
```

`perceived_effort` is optional and must be `easy`, `moderate`, or `hard`.
<img width="1435" height="765" alt="Runs" src="https://github.com/user-attachments/assets/94babaaf-782d-4a94-bc57-1ac66eb87b84" />
<img width="1427" height="774" alt="New run" src="https://github.com/user-attachments/assets/457658f7-0dae-4eb4-9331-53df0a4e99df" />
<img width="1413" height="772" alt="Edit run" src="https://github.com/user-attachments/assets/2608be94-af5c-4134-89e3-c01ed3da9685" />
## Pages

| Page | Purpose |
| --- | --- |
| `/` | Redirects to the dashboard or the login page |
| `/register.html`, `/login.html` | Account creation and sign-in |
| `/dashboard.html` | Totals, pace by category, personal records |
| `/runs.html` | Run list with edit and delete |
| `/run_new.html`, `/run_edit.html?id=<id>` | Log or edit a run |
| `/profile.html` | Edit your profile |

## Project structure

```
backend/
  app/
    models/      SQLAlchemy models (User, Profile, Run, PersonalRecord)
    routes/      Flask blueprints (auth, profile, runs, records, dashboard)
    schemas/     marshmallow validation schemas
    services/    Pace calculation, distance matching, personal-record logic
    static/      The frontend pages and the shared api.js helper
  migrations/    Alembic migrations
  tests/         pytest suite
```
