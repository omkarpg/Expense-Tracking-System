import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"


def analytics_by_month():
    # ------------------ Title ------------------
    st.title("📊 Monthly Expense Analytics")
    st.caption("Visual overview of your expenses month-wise")

    st.divider()

    # ------------------ API Call ------------------
    response = requests.get(f"{API_URL}/analytics_by_month/")

    if response.status_code != 200:
        st.error("❌ Failed to fetch data from API")
        return

    data = response.json()

    if not data:
        st.warning("⚠️ No expense data available")
        return

    # ------------------ DataFrame ------------------
    df = pd.DataFrame(data)

    # Expected keys: Month, Month_no, Total_amount
    df = df.sort_values("Month_no")

    # ------------------ Metrics ------------------
    total_expense = df["Total_amount"].sum()
    avg_expense = df["Total_amount"].mean()
    max_month = df.loc[df["Total_amount"].idxmax(), "Month"]

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Expense", f"₹ {total_expense:,.0f}")
    col2.metric("📉 Avg / Month", f"₹ {avg_expense:,.0f}")
    col3.metric("🏆 Highest Spend", max_month)

    st.divider()

    # ------------------ Bar Chart ------------------
    st.subheader("📅 Expense Breakdown by Month")

    chart_df = df.set_index("Month")["Total_amount"]
    st.bar_chart(chart_df)

    # ------------------ Data Table ------------------
    with st.expander("📋 View Detailed Data"):
        st.dataframe(
            df[["Month", "Total_amount"]],
            use_container_width=True,
            hide_index=True
        )