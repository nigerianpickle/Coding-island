import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import sqlite3

# --- 1. Create data folder ---
os.makedirs("data", exist_ok=True)

# --- 2. Generate sample dataset ---
fake = Faker()
random.seed(42)

engine_types = ["PW200", "CF34", "CFM56", "GE90"]
technicians = ["Alex", "Jordan", "Emily", "Ravi", "Mei", "Sophie"]

rows = []
start_date = datetime(2025, 1, 1)

for i in range(120):
    job_id = f"J{i:03d}"
    engine = random.choice(engine_types)
    tech = random.choice(technicians)
    cost = random.randint(10000, 25000)
    turnaround = random.randint(7, 20)
    parts = random.randint(20, 40)
    completed = start_date + timedelta(days=random.randint(0, 300))
    rows.append([job_id, engine, tech, cost, turnaround, parts, completed.date()])

df = pd.DataFrame(rows, columns=[
    "job_id", "engine_type", "technician", "cost_usd",
    "turnaround_days", "parts_used", "completed_date"
])
df.to_csv("data/maintenance_jobs.csv", index=False)
print("✅ Dataset created and saved in /data.")

# --- 3. Load data into SQLite & run SQL analysis ---
conn = sqlite3.connect("maintenance.db")
df = pd.read_csv("data/maintenance_jobs.csv")
df.to_sql("maintenance_jobs", conn, if_exists="replace", index=False)

query = """
SELECT engine_type, 
       ROUND(AVG(cost_usd), 2) AS avg_cost,
       ROUND(AVG(turnaround_days), 2) AS avg_turnaround
FROM maintenance_jobs
GROUP BY engine_type
ORDER BY avg_cost DESC;
"""

result = pd.read_sql_query(query, conn)
print("\n--- Average Cost and Turnaround by Engine Type ---")
print(result)

conn.close()
