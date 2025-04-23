import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

# Load sector and fund flow data
df = pd.read_csv("data/flows_raw.csv")
flow_df = pd.read_csv("data/fund_flows.csv", parse_dates=["date"])

st.header("🔁 Compare Two ETFs Side-by-Side")

# ETF dropdowns
col1, col2 = st.columns(2)
with col1:
    left_etf = st.selectbox("Select First ETF", sorted(df["ticker"].unique()), key="left")
with col2:
    right_etf = st.selectbox("Select Second ETF", sorted(df["ticker"].unique()), key="right")

# Filter sector breakdown
left_sector = df[df["ticker"] == left_etf][["sector", "weight_percentage"]].sort_values("weight_percentage", ascending=False)
right_sector = df[df["ticker"] == right_etf][["sector", "weight_percentage"]].sort_values("weight_percentage", ascending=False)

# Filter and roll fund flows
left_flow = flow_df[flow_df["ticker"] == left_etf].sort_values("date")
right_flow = flow_df[flow_df["ticker"] == right_etf].sort_values("date")
left_flow["rolling_avg"] = left_flow["net_flow_usd"].rolling(7).mean()
right_flow["rolling_avg"] = right_flow["net_flow_usd"].rolling(7).mean()

# --- Sector Allocation Bar Charts ---
st.subheader(f"📊 Sector Allocation: {left_etf} vs {right_etf}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

ax1.barh(left_sector["sector"], left_sector["weight_percentage"], color="#1f77b4")
ax1.set_title(left_etf)
ax1.set_xlim(0, 40)
ax1.set_xlabel("Weight (%)")
ax1.set_xticks(range(0, 45, 5))
ax1.grid(axis='x', linestyle='--', alpha=0.5)
ax1.invert_yaxis()

ax2.barh(right_sector["sector"], right_sector["weight_percentage"], color="#ff7f0e")
ax2.set_title(right_etf)
ax2.set_xlim(0, 40)
ax2.set_xlabel("Weight (%)")
ax2.set_xticks(range(0, 45, 5))
ax2.grid(axis='x', linestyle='--', alpha=0.5)
ax2.invert_yaxis()

st.pyplot(fig)

# --- Fund Flows Line Chart ---
st.subheader(f"📉 Fund Flows: {left_etf} vs {right_etf} (7-day Rolling Avg, Millions USD)")

merged_flows = pd.merge(
    left_flow[["date", "rolling_avg"]].rename(columns={"rolling_avg": f"{left_etf}"}),
    right_flow[["date", "rolling_avg"]].rename(columns={"rolling_avg": f"{right_etf}"}),
    on="date", how="outer"
).set_index("date").sort_index()

merged_flows_mil = merged_flows / 1_000_000  # convert to millions

st.line_chart(merged_flows_mil)