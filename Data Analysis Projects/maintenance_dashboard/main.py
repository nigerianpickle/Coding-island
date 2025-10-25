# main.py  (data generation section)
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

engine_types = ["PW200", "CF34", "CFM56", "GE90"]
technicians = ["Alex", "Jordan", "Emily", "Ravi", "Mei", "Sophie"]

rows = []
start_date = datetime(2025, 1, 1)

for i in range(120):  # 120 maintenance jobs
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
print("✅ Data generated.")
