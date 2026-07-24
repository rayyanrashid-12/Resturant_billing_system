import streamlit as st
from api import get_reports

def dashboard_page():

    st.header("🏠 Dashboard")

    response = get_reports(st.session_state.token)

    if response.status_code == 200:

        report = response.json()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Orders",
                report["total_orders"]
            )

        with col2:
            st.metric(
                "Total Sales",
                f"Rs. {report['total_sales']}"
            )

    else:
        st.error("Unable to load dashboard.")