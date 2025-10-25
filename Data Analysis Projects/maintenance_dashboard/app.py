import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/maintenance_jobs.csv")
df["completed_date"] = pd.to_datetime(df["completed_date"])
df["month"] = df["completed_date"].dt.to_period("M")

st.title("Maintenance Insights Dashboard")

col1, col2 = st.columns(2)
col1.metric("Average Cost", f"${df['cost_usd'].mean():,.0f}")
col2.metric("Average Turnaround", f"{df['turnaround_days'].mean():.1f} days")

fig = px.line(df.groupby("month")["cost_usd"].sum().reset_index(),
              x="month", y="cost_usd", title="Monthly Maintenance Cost")
st.plotly_chart(fig)

engine_chart = px.bar(df, x="engine_type", y="turnaround_days",
                      title="Avg Turnaround by Engine Type", 
                      color="engine_type", barmode="group")
st.plotly_chart(engine_chart)
