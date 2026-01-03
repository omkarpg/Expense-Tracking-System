import streamlit as st
from add_update_ui import add_update
from analytics_ui import analytics_tab
from analytics_by_months import analytics_by_month

API_URL = "http://localhost:8000"

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Expense Management System",
    page_icon="💰",
    layout="wide"
)

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
h1, h2, h3 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
st.sidebar.title("💰 Expense Manager")
st.sidebar.caption("Track • Analyze • Control")

menu = st.sidebar.radio(
    "Navigation",
    ["➕ Add / Update", "📊 Analytics by Category", "📅 Analytics by Month"]
)

# ------------------ Header ------------------
st.title("💰 Expense Management System")
st.caption("A simple and smart way to manage your expenses")
st.divider()

# ------------------ Navigation Logic ------------------
if menu == "➕ Add / Update":
    add_update()

elif menu == "📊 Analytics by Category":
    analytics_tab()

elif menu == "📅 Analytics by Month":
    analytics_by_month()
