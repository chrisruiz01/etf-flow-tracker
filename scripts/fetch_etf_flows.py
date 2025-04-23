import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

tickers = ["SPY", "ARKK", "QQQ", "XLF", "XLE"]
all_data = []

for ticker in tickers:
    url = f"https://financialmodelingprep.com/api/v3/etf-sector-weightings/{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Response for {ticker}: {data}")
        for item in data:
            all_data.append({
                "ticker": ticker,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "sector": item.get("sector"),
                "weight_percentage": item.get("weightPercentage")
            })

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(all_data)
df.to_csv("data/flows_raw.csv", index=False)
print("Data saved to data/flows_raw.csv")

# Simulated daily fund flows
flow_data = []
dates = pd.date_range(end=datetime.now(), periods=30)

for ticker in tickers:
    base = np.random.normal(loc=0, scale=5, size=len(dates)) * 1e6  # simulate $ inflows/outflows
    for date, flow in zip(dates, base):
        flow_data.append({
            "ticker": ticker,
            "date": date.strftime("%Y-%m-%d"),
            "net_flow_usd": round(flow, 2)
        })

flow_df = pd.DataFrame(flow_data)
os.makedirs("data", exist_ok=True)
flow_df.to_csv("data/fund_flows.csv", index=False)
print("Fund flow data saved to data/fund_flows.csv")
