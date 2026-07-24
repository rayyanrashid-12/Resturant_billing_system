import streamlit as st
from api import (
    create_order,
    get_orders,
    get_menu,
    add_item_to_order,
)

def orders_page():

    st.header("🛒 Order Management")

    # ---------------- Create Order ----------------

    st.subheader("Create New Order")

    customer_name = st.text_input(
        "Customer Name",
        key="order_customer"
    )

    if st.button(
        "Create Order",
        key="create_order_btn"
    ):

        response = create_order(
            st.session_state.token,
            customer_name
        )

        if response.status_code == 200:

            st.session_state.order_id = response.json()["id"]

            st.success("Order Created Successfully!")

            st.rerun()

        else:

            st.error(response.text)

    st.divider()

    # ---------------- Orders ----------------

    response = get_orders(st.session_state.token)

    if response.status_code == 200:

        orders = response.json()

        if orders:
            st.dataframe(
                orders,
                use_container_width=True
            )

        else:
            st.info("No Orders Yet")

    st.divider()

    # ---------------- Add Item ----------------

    st.subheader("Add Item To Order")

    menu_response = get_menu(st.session_state.token)

    if menu_response.status_code == 200:

        menu = menu_response.json()

        if len(menu) == 0:

            st.warning("No menu available.")

            return

        menu_options = {
            f"{item['name']} - Rs.{item['price']}": item["id"]
            for item in menu
        }

        selected_item = st.selectbox(
            "Select Menu Item",
            list(menu_options.keys()),
            key="order_menu"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            key="order_qty"
        )

        if st.button(
            "Add Item",
            key="add_item_btn"
        ):

            if st.session_state.order_id is None:

                st.warning("Create an order first.")

            else:

                response = add_item_to_order(
                    st.session_state.token,
                    st.session_state.order_id,
                    menu_options[selected_item],
                    quantity
                )

                if response.status_code == 200:

                    st.success("Item Added Successfully!")

                    st.rerun()

                else:

                    st.error(response.text)