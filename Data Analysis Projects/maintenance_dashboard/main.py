import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

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

# Load data
df = pd.read_csv("data/maintenance_jobs.csv")
df["completed_date"] = pd.to_datetime(df["completed_date"])

# --- 1. Trend: Total monthly maintenance cost ---
df["month"] = df["completed_date"].dt.to_period("M")
monthly_cost = df.groupby("month")["cost_usd"].sum().reset_index()

plt.figure(figsize=(8,4))
monthly_cost["month"] = monthly_cost["month"].astype(str)
sns.lineplot(data=monthly_cost, x="month", y="cost_usd", marker="o")
plt.title("Monthly Maintenance Cost Trend")
plt.ylabel("Total Cost (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_trend.png")
plt.show()

# --- 2. Avg turnaround by engine type ---
plt.figure(figsize=(6,4))
sns.barplot(data=df, x="engine_type", y="turnaround_days", estimator="mean", ci=None)
plt.title("Average Turnaround Days by Engine Type")
plt.ylabel("Days")
plt.tight_layout()
plt.savefig("turnaround_engine.png")
plt.show()

# --- 3. Cost vs Turnaround scatter ---
sns.scatterplot(data=df, x="turnaround_days", y="cost_usd", hue="engine_type")
plt.title("Cost vs Turnaround Time")
plt.savefig("scatter_cost_turnaround.png")
plt.show()