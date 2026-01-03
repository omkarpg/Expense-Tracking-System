import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"


def add_update():
    # ------------------ Title ------------------
    st.title("➕ Add / Update Expenses")
    st.caption("Add or modify your daily expenses easily")

    st.divider()

    # ------------------ Date Selection ------------------
    selected_date = st.date_input(
        "Select Date",
        datetime(2024, 8, 1)
    )
    selected_date_str = selected_date.isoformat()

    # ------------------ Fetch Existing Expenses ------------------
    response = requests.get(f"{API_URL}/expenses/{selected_date_str}")

    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("❌ Failed to retrieve expenses")
        existing_expenses = []

    # ------------------ Categories ------------------
    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # ------------------ Expense Form ------------------
    with st.form("expense_form"):
        st.subheader("🧾 Expense Details")

        header_col1, header_col2, header_col3 = st.columns(3)
        header_col1.markdown("**💰 Amount**")
        header_col2.markdown("**📂 Category**")
        header_col3.markdown("**📝 Notes**")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i].get("amount", 0.0)
                category = existing_expenses[i].get("category", "Shopping")
                notes = existing_expenses[i].get("notes", "")
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )

            with col2:
                category_input = st.selectbox(
                    "Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    "Notes",
                    value=notes,
                    key=f"notes_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        st.divider()

        submit_button = st.form_submit_button("💾 Save Expenses")

        if submit_button:
            filtered_expenses = [
                expense for expense in expenses if expense["amount"] > 0
            ]

            if not filtered_expenses:
                st.warning("⚠️ Please enter at least one expense")
                return

            response_update = requests.post(
                f"{API_URL}/expenses/{selected_date_str}",
                json=filtered_expenses
            )

            if response_update.status_code == 200:
                st.success("✅ Expenses updated successfully")
            else:
                st.error("❌ Failed to update expenses")
