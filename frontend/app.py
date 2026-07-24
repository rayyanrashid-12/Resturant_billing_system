import streamlit as st

from pages.dashboard import dashboard_page
from pages.menu import menu_page
from pages.orders import orders_page
from pages.billing import billing_page
from pages.reports import reports_page
from pages.login import login_page

st.set_page_config(
    page_title="Restaurant Billing System",
    layout="wide"
)

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    login_page()

else:
    st.sidebar.title("Restaurant Billing")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Menu",
            "Orders",
            "Billing",
            "Reports",
        ],
    )

    if page == "Dashboard":
        dashboard_page()

    elif page == "Menu":
        menu_page()

    elif page == "Orders":
        orders_page()

    elif page == "Billing":
        billing_page()

    elif page == "Reports":
        reports_page()