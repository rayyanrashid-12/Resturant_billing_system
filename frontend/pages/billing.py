import streamlit as st
from api import get_orders, get_bill

def billing_page():

    st.header("🧾 Billing")

    response = get_orders(st.session_state.token)

    if response.status_code != 200:
        st.error(response.text)
        return

    orders = response.json()

    if not orders:
        st.info("No Orders Available")
        return

    order_dict = {
        f"Order #{o['id']} - {o['customer_name']}": o["id"]
        for o in orders
    }

    selected = st.selectbox(
        "Select Order",
        list(order_dict.keys()),
        key="billing_order"
    )

    if st.button(
        "Generate Bill",
        key="generate_bill"
    ):

        response = get_bill(
            st.session_state.token,
            order_dict[selected]
        )

        if response.status_code == 200:

            bill = response.json()

            st.success("Bill Generated")

            st.subheader("Invoice")

            st.write(f"Customer : {bill['customer_name']}")
            st.write(f"Order ID : {bill['order_id']}")

            st.metric(
                "Subtotal",
                f"Rs. {bill['subtotal']:.2f}"
            )

            st.metric(
                "Tax (10%)",
                f"Rs. {bill['tax']:.2f}"
            )

            st.metric(
                "Grand Total",
                f"Rs. {bill['grand_total']:.2f}"
            )

            st.write(
                f"Status : {bill['status']}"
            )

        else:
            st.error(response.text)