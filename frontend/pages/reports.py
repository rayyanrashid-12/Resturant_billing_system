import streamlit as st
from api import get_reports

def reports_page():

    st.header("📊 Reports")

    response = get_reports(st.session_state.token)

    if response.status_code != 200:
        st.error(response.text)
        return

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
            f"Rs. {report['total_sales']:.2f}"
        )

    st.divider()

    st.bar_chart(
        {
            "Sales": [report["total_sales"]]
        }
    )

    st.bar_chart(
        {
            "Orders": [report["total_orders"]]
        }
    )