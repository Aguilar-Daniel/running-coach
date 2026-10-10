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
<img width="1438" height="774" alt="Register page" src="https://github.com/user-attachments/assets/90772331-2177-4c2d-8d6e-7fdf5cd4e493" />

<img width="1440" height="781" alt="Login page" src="https://github.com/user-attachments/assets/bedb1e55-9a9e-479e-b521-3d29b2863baf" />



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

<img width="1436" height="762" alt="Dashboard" src="https://github.com/user-attachments/assets/981f84bb-3d67-433e-9c86-2e4e75993995" />


<img width="1440" height="779" alt="Profile" src="https://github.com/user-attachments/assets/be7fc0e5-e16f-4b9d-8377-bdb5c5b04a7a" />


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

<img width="1435" height="765" alt="Runs" src="https://github.com/user-attachments/assets/cf69180e-e03b-4c14-833e-40afe06fdc9a" />

<img width="1427" height="774" alt="New run" src="https://github.com/user-attachments/assets/4b96ff1a-f3d4-4ab7-a829-7a39f1e0f881" />

<img width="1413" height="772" alt="Edit run" src="https://github.com/user-attachments/assets/15b9e88f-3918-44de-8d80-39c956c26e4e" />


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
