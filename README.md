# own-repo-F26

Class survey data loaded into PostgreSQL on Railway.

## Tables

- `students` — one row per person
- `tools` — programming / data tools
- `availability` — weekday and weekend time slots
- `student_tools` — student ↔ tools
- `student_availability` — student ↔ time slots

## Setup

Set `DATABASE_URL` in a local `.env` file to the Railway **public** Postgres URL. That file is gitignored and should not be committed.

Local run:

```bash
source venv/Scripts/activate
python app.py
```

## Deploy on Railway

1. Push this repo to GitHub.
2. In Railway, create a service from the GitHub repo. Railway will use the `Dockerfile`.
3. Link the Postgres service and set `DATABASE_URL` to the Postgres variable (internal URL is fine on Railway).
4. Railway injects `PORT`; gunicorn binds to `0.0.0.0:$PORT`.
