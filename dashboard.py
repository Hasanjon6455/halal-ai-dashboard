
import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="📈 Halal Trade Dashboard", layout="wide")
st.title("📈 Halal AI Trading Bot - Weekly Reports")

report_dir = "Reports"
files = sorted([f for f in os.listdir(report_dir) if f.endswith(".csv")], reverse=True)

if not files:
    st.warning("No reports found in the Reports folder.")
else:
    selected_file = st.selectbox("📁 Select a report to view:", files)
    df = pd.read_csv(os.path.join(report_dir, selected_file))

    st.markdown(f"#### 🗓️ Report Date: {selected_file.replace('.csv', '')}")
    st.divider()

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Total Stocks", len(df))
    col2.metric("🟢 Buy Orders", (df['Decision'] == 'BUY $5').sum())
    col3.metric("🔴 Sell Orders", (df['Decision'] == 'SELL $10').sum())
    col4.metric("⚠️ Failed Trades", df['Memo'].str.contains('fail', case=False, na=False).sum() if 'Memo' in df.columns else 0)

    tab1, tab2, tab3 = st.tabs(["📋 Table", "📈 Charts", "🧰 Error Filter"])

    with tab1:
        st.subheader("📄 Raw Trade Data")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("📊 Trade Charts")
        if "Decision" in df.columns:
            st.plotly_chart(
                px.pie(df, names="Decision", title="Trade Decisions"),
                use_container_width=True
            )
        if "Price Change (%)" in df.columns:
            st.plotly_chart(
                px.histogram(df, x="Price Change (%)", nbins=20, title="Price Change Distribution"),
                use_container_width=True
            )

    with tab3:
        st.subheader("🔍 Filter Trades by Memo (Errors, Notes)")
        if "Memo" in df.columns:
            keyword = st.text_input("Enter a keyword (e.g. 'fail', '404', 'boycott')")
            if keyword:
                filtered_df = df[df["Memo"].str.contains(keyword, case=False, na=False)]
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No 'Memo' column found in this report.")
