import streamlit as st
from api import (
    get_menu,
    create_menu,
    delete_menu,
)

def menu_page():

    st.header("🍔 Menu Management")

    response = get_menu(st.session_state.token)

    if response.status_code == 200:

        menu = response.json()

        if menu:
            st.subheader("Current Menu")
            st.table(menu)
        else:
            st.info("No menu items available.")

    st.divider()

    st.subheader("Add Menu Item")

    name = st.text_input("Item Name")
    description = st.text_input("Description")
    price = st.number_input("Price", min_value=0.0)
    category = st.text_input("Category")

    if st.button("Add Item"):

        data = {
            "name": name,
            "description": description,
            "price": price,
            "category": category
        }

        result = create_menu(
            st.session_state.token,
            data
        )

        if result.status_code == 200:
            st.success("Menu Item Added")
            st.rerun()
        else:
            st.error(result.text)

    st.divider()

    st.subheader("Delete Menu Item")

    delete_id = st.number_input(
        "Item ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Item"):

        result = delete_menu(
            st.session_state.token,
            delete_id
        )

        if result.status_code == 200:
            st.success("Item Deleted")
            st.rerun()
        else:
            st.error(result.text)