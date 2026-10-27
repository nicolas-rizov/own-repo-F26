import os
from flask import Flask, render_template
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Fetch database URL safely from environment
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not set")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)

AVG_QUERY = """
    SELECT
        AVG(skill_programming),
        AVG(skill_data_stats),
        AVG(skill_frontend_design),
        AVG(skill_business_pitch)
    FROM {table}
"""


def fetch_class_page(conn, table):
    names = [
        row[0]
        for row in conn.execute(text(f"SELECT name FROM {table}"))
        if row[0]
    ]
    avg_row = conn.execute(text(AVG_QUERY.format(table=table))).one()
    averages = {
        "programming": round(float(avg_row[0]), 2) if avg_row[0] is not None else None,
        "data_stats": round(float(avg_row[1]), 2) if avg_row[1] is not None else None,
        "frontend_design": round(float(avg_row[2]), 2) if avg_row[2] is not None else None,
        "business_pitch": round(float(avg_row[3]), 2) if avg_row[3] is not None else None,
    }
    return names, averages


@app.route("/")
def index():
    with engine.connect() as conn:
        try:
            names, averages = fetch_class_page(conn, "students")
        except Exception:
            names, averages = fetch_class_page(conn, "class_dataset")

    return render_template("index.html", names=names, averages=averages)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")