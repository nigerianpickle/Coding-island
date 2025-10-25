import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Maintenance Insights Dashboard", layout="wide")

# --- Load Data ---
df = pd.read_csv("data/maintenance_jobs.csv")
df["completed_date"] = pd.to_datetime(df["completed_date"])
df["month"] = df["completed_date"].dt.to_period("M").astype(str)

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
engine_filter = st.sidebar.multiselect(
    "Select Engine Type(s):",
    options=df["engine_type"].unique(),
    default=df["engine_type"].unique()
)
tech_filter = st.sidebar.multiselect(
    "Select Technician(s):",
    options=df["technician"].unique(),
    default=df["technician"].unique()
)

df_filtered = df[df["engine_type"].isin(engine_filter) & df["technician"].isin(tech_filter)]

# --- KPI Metrics ---
avg_cost = df_filtered["cost_usd"].mean()
avg_turnaround = df_filtered["turnaround_days"].mean()

st.title("🔧 Maintenance Insights Dashboard")
st.markdown("Analyze aircraft maintenance trends, costs, and technician efficiency.")

col1, col2 = st.columns(2)
col1.metric("Average Cost", f"${avg_cost:,.0f}")
col2.metric("Average Turnaround", f"{avg_turnaround:.1f} days")

# --- Monthly Cost Trend ---
df_filtered["month"] = df_filtered["completed_date"].dt.to_period("M").astype(str)
monthly_cost = df_filtered.groupby("month")["cost_usd"].sum().reset_index()

fig1 = px.line(monthly_cost, x="month", y="cost_usd", markers=True,
               title="Monthly Maintenance Cost Trend", labels={"cost_usd": "Total Cost (USD)"})
st.plotly_chart(fig1, use_container_width=True)

# --- Avg Turnaround by Engine Type ---
turnaround_chart = df_filtered.groupby("engine_type")["turnaround_days"].mean().reset_index()
fig2 = px.bar(turnaround_chart, x="engine_type", y="turnaround_days",
              title="Average Turnaround Days by Engine Type",
              color="engine_type", text_auto=".1f")
st.plotly_chart(fig2, use_container_width=True)

# --- Cost vs Turnaround Scatter ---
fig3 = px.scatter(df_filtered, x="turnaround_days", y="cost_usd", color="engine_type",
                  title="Cost vs Turnaround Time", hover_data=["technician"])
st.plotly_chart(fig3, use_container_width=True)

st.caption("Built with Streamlit • Data simulated for demonstration • Author: Daniel Nwogo")
