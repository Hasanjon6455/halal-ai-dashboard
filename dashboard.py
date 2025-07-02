import streamlit as st
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load environment variables
load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")


api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version="v2")

# Set Streamlit page settings
st.set_page_config(page_title="📈 Halal Trade Dashboard", layout="wide")
st.title("📊 Halal AI Trading Bot - Weekly Reports")

# -----------------------------
# 💼 Portfolio Summary Section
# -----------------------------
st.header("💼 Portfolio Summary")

try:
    account = api.get_account()
    positions = api.list_positions()

    net_invested = sum(float(pos.cost_basis) for pos in positions)
    current_value = sum(float(pos.market_value) for pos in positions)
    change_value = current_value - net_invested
    change_percent = (change_value / net_invested) * 100 if net_invested != 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Net Invested", f"${net_invested:,.2f}")
    col2.metric("Current Value", f"${current_value:,.2f}")
    col3.metric("P/L %", f"{change_percent:+.2f}%")

except Exception as e:
    st.warning("Could not fetch Alpaca data. Check API keys.")
    st.text(f"Error: {e}")

# -----------------------------
# 📁 Weekly Trade Report Viewer
# -----------------------------
st.header("📁 Weekly Trade Reports")

report_dir = "Reports"
files = sorted([f for f in os.listdir(report_dir) if f.endswith(".csv")], reverse=True)

if not files:
    st.warning("No reports found in the Reports folder.")
else:
    selected_file = st.selectbox("📂 Select a report to view:", files)
    df = pd.read_csv(os.path.join(report_dir, selected_file))

    st.markdown(f"### 📅 Report Date: **{selected_file.replace('.csv', '')}**")
    st.divider()

    # Summary metrics
    st.markdown("### 📊 Summary Stats")
    st.write(df.describe(include='all'))

    # Pie chart for decisions
    if "Decision" in df.columns:
        st.plotly_chart(px.pie(df, names="Decision", title="Trade Decisions"))

    # Histogram for price changes
    if "Price Change (%)" in df.columns:
        st.plotly_chart(px.histogram(df, x="Price Change (%)", nbins=20, title="Price Change Distribution"))

    # Filter by memo keywords (optional)
    if "Memo" in df.columns:
        keyword = st.text_input("🔍 Filter by Memo Keyword (e.g., 'fail', '404'):")
        if keyword:
            df = df[df["Memo"].str.contains(keyword, case=False, na=False)]

    st.dataframe(df, use_container_width=True)
