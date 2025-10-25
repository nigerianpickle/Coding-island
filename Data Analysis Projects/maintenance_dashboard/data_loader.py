import sqlite3

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
print(result)
