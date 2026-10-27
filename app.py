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
    raise ValueError("DATABASE_URL is not set in .env")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)

@app.route("/")
def index():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT name FROM students"))
            names = [row[0] for row in result if row[0]]
        except Exception:
            # Fallback if your table is named class_dataset
            result = conn.execute(text("SELECT name FROM class_dataset"))
            names = [row[0] for row in result if row[0]]

    return render_template("index.html", names=names)

if __name__ == "__main__":
    app.run(debug=True, port=5000)