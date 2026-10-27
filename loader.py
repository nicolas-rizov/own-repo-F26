import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not set in your .env file!")

# Convert postgres:// to postgresql:// for SQLAlchemy compatibility
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

print("Connecting to Railway PostgreSQL...")
engine = create_engine(db_url)

# 1. Execute SQL schema to create tables/enums
schema_path = os.path.join("Data", "class_dataset.sql")
if os.path.exists(schema_path):
    print(f"Applying schema from {schema_path}...")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    with engine.connect() as conn:
        conn.execute(text(sql_content))
        conn.commit()
    print("Schema applied successfully.")
else:
    print(f"Warning: {schema_path} not found.")

# 2. Load CSV data into PostgreSQL
csv_path = os.path.join("Data", "class_dataset.csv")
if os.path.exists(csv_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    df.to_sql("class_dataset", engine, if_exists="append", index=False)
    print("Data successfully loaded into Railway PostgreSQL!")
else:
    print(f"Error: {csv_path} not found.")