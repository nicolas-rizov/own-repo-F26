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
