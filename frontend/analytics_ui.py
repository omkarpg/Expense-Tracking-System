import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"


def analytics_tab():
    # ------------------ Title ------------------
    st.title("📊 Category-wise Expense Analytics")
    st.caption("Analyze your expenses by category within a date range")

    st.divider()

    # ------------------ Date Filters ------------------
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime(2024, 8, 1)
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            datetime(2024, 8, 5)
        )

    st.divider()

    # ------------------ Fetch Analytics ------------------
    if st.button("📈 Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)

        if response.status_code != 200:
            st.error("❌ Failed to fetch analytics")
            return

        response_data = response.json()

        if not response_data:
            st.warning("⚠️ No data available for selected date range")
            return

        # ------------------ DataFrame ------------------
        df = pd.DataFrame({
            "Category": response_data.keys(),
            "Total": [response_data[c]["total"] for c in response_data],
            "Percentage": [response_data[c]["percentage"] for c in response_data]
        })

        df = df.sort_values("Percentage", ascending=False)

        # ------------------ Metrics ------------------
        total_spent = df["Total"].sum()
        top_category = df.iloc[0]["Category"]

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Expense", f"₹ {total_spent:,.0f}")
        col2.metric("🏆 Top Category", top_category)
